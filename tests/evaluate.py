"""
Make extraction results comparable with other libraries of the same kind.
"""

import argparse
import logging
import os
import sys
import time

from contextlib import suppress
from dataclasses import dataclass
from functools import cache, partial
from importlib.metadata import PackageNotFoundError, version

import justext
import pandas as pd
import tqdm

from eval_common import EXTRACT_OPTS, ConfusionMatrix, load_evaldata, make_runners, read_document, run_and_count, validate

from trafilatura import baseline, extract, html2txt
from trafilatura.external import jt_stoplist_init

# for run_custom
from justext.core import ParagraphMaker, classify_paragraphs, revise_paragraph_classification
from trafilatura.baseline import basic_cleaning
from trafilatura.utils import load_html


# Competitors are imported in their runner, so a missing one only disables its own
# algorithm (see resolve_versions). justext is a Trafilatura dependency, always there.

JT_STOPLIST = jt_stoplist_init()

HERE = os.path.abspath(os.path.dirname(__file__))


@cache
def get_detect():
    try:
        from cchardet import detect
    except ImportError:
        from charset_normalizer import detect
    return detect


@cache
def get_boilerpipe():
    from boilerpy3 import extractors

    return extractors.ArticleExtractor()  # ArticleExtractor DefaultExtractor LargestContentExtractor


@cache
def get_goose():
    from goose3 import Goose

    return Goose()


@cache
def get_magic_html():
    from magic_html import GeneralExtractor

    return GeneralExtractor()


def convert_to_str(htmlbinary):
    "Conversion and encoding fix for the tests."
    try:
        guessed_encoding = get_detect()(htmlbinary)["encoding"]
        htmlstring = htmlbinary.decode(guessed_encoding)
    except (TypeError, UnicodeDecodeError):
        htmlstring = htmlbinary
    return htmlstring


def run_custom(htmlbinary):
    tree = basic_cleaning(load_html(htmlbinary))
    paragraphs = ParagraphMaker.make_paragraphs(tree)
    classify_paragraphs(paragraphs, JT_STOPLIST, 50, 150, 0.1, 0.2, 0.3, True)
    revise_paragraph_classification(paragraphs, 150)
    return " ".join([p.text for p in paragraphs if not p.is_boilerplate])


def run_baseline(htmlbinary):
    """run bare text extraction within lxml"""
    _, result, _ = baseline(htmlbinary)
    return result


def run_justext(htmlbinary):
    """try with the generic algorithm justext"""
    paragraphs = justext.justext(htmlbinary, JT_STOPLIST, 50, 200, 0.1, 0.2, 0.2, 200, True)  # stop_words
    valid = [paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate]

    return " ".join(valid)


def run_goose(htmlbinary):
    """try with the goose algorithm"""
    return get_goose().extract(raw_html=htmlbinary).cleaned_text


def run_readability(htmlbinary):
    """try with the Python3 port of readability.js"""
    from readability import Document

    return Document(convert_to_str(htmlbinary)).summary()


def run_inscriptis(htmlbinary):
    """try with the inscriptis module"""
    from inscriptis import get_text

    return get_text(convert_to_str(htmlbinary))


def run_html2text(htmlbinary):
    """try with the html2text module"""
    import html2text

    return html2text.html2text(convert_to_str(htmlbinary))


def run_html_text(htmlbinary):
    """try with the html_text module"""
    import html_text

    return html_text.extract_text(convert_to_str(htmlbinary), guess_layout=False)


def run_boilerpipe(htmlbinary):
    """try with the boilerpipe algorithm"""
    return get_boilerpipe().get_content(convert_to_str(htmlbinary))


def run_newspaper(htmlbinary):
    """try with the newspaper package"""
    from newspaper import fulltext

    return fulltext(htmlbinary)


def run_newsplease(htmlbinary):
    """try with newsplease"""
    from newsplease import NewsPlease

    # fetch_images=False: the default fetches images from each article's live host
    return NewsPlease.from_html(convert_to_str(htmlbinary), url=None, fetch_images=False).maintext


def run_resiliparse(htmlbinary):
    """try with the resiliparse package"""
    from resiliparse.extract.html2text import extract_plain_text
    from resiliparse.parse.encoding import bytes_to_str, detect_encoding
    from resiliparse.parse.html import HTMLTree

    try:
        htmlstring = bytes_to_str(htmlbinary, detect_encoding(htmlbinary))
    except TypeError:  # already a string
        htmlstring = htmlbinary
    tree = HTMLTree.parse(htmlstring)
    return extract_plain_text(tree, main_content=True)


def run_bs4(htmlbinary):
    """try with the BeautifulSoup module"""
    from bs4 import BeautifulSoup

    return BeautifulSoup(htmlbinary, features="lxml").get_text(strip=True)


def run_magic_html(htmlbinary):
    """try with the magic_html package"""
    return run_bs4(get_magic_html().extract(convert_to_str(htmlbinary), base_url="").get("html"))


@dataclass
class BenchmarkMatrix(ConfusionMatrix):
    "Shared confusion matrix plus per-algorithm timing and skip bookkeeping."

    time: float = 0.0
    skipped: int = 0


def timed(fn, matrix):
    "Time the extraction only, not run_and_count's scoring."

    def wrapper(htmlbinary):
        start = time.perf_counter()
        try:
            return fn(htmlbinary)
        finally:
            matrix.time += time.perf_counter() - start

    return wrapper


# marks a "library" with no version to look up
NO_LIBRARY = "-"

# canonical trafilatura runners, shared with eval_gate.py so the CI gate can't drift
RUNNERS = make_runners(extract)

# algorithm string, package, function, results
ALGORITHMS = {
    "everything": {"library": NO_LIBRARY, "function": convert_to_str},
    "nothing": {"library": NO_LIBRARY, "function": lambda htmlbinary: ""},
    "custom": {"library": NO_LIBRARY, "function": run_custom},
    "baseline": {"library": NO_LIBRARY, "function": run_baseline},
    "html2txt": {"library": NO_LIBRARY, "function": html2txt},
    "trafilatura fast": {"library": "trafilatura", "function": RUNNERS["fast"]},
    "trafilatura": {"library": "trafilatura", "function": RUNNERS["fallback"]},
    "html2text": {"library": "html2text", "function": run_html2text},
    "html_text": {"library": "html_text", "function": run_html_text},
    "inscriptis": {"library": "inscriptis", "function": run_inscriptis},
    "justext": {"library": "justext", "function": run_justext},
    "goose": {"library": "goose3", "function": run_goose},
    "newspaper": {"library": "newspaper4k", "function": run_newspaper},
    "boilerpipe": {"library": "boilerpy3", "function": run_boilerpipe},
    "newsplease": {"library": "news-please", "function": run_newsplease},
    "readability": {"library": "readability-lxml", "function": run_readability},
    "resiliparse": {"library": "resiliparse", "function": run_resiliparse},
    "bs4": {"library": "beautifulsoup4", "function": run_bs4},
    "magic_html": {"library": "magic_html", "function": run_magic_html},
    "trafilatura precision": {
        "library": "trafilatura",
        "function": partial(extract, fast=False, favor_precision=True, **EXTRACT_OPTS),
    },
    "trafilatura recall": {
        "library": "trafilatura",
        "function": partial(extract, fast=False, favor_recall=True, **EXTRACT_OPTS),
    },
}

# fixed order, matching what ConfusionMatrix.scores() returns
METRICS = ["precision", "recall", "accuracy", "f1"]

# next to the script, not relative to the working directory
OUTPUT_DIR = os.path.join(HERE, "results")


def resolve_versions(algorithms):
    "{algorithm: version} for the installed ones, in output order; the rest are dropped."
    versions = {}
    for algo in algorithms:
        library = ALGORITHMS[algo]["library"]
        if library == NO_LIBRARY:
            versions[algo] = NO_LIBRARY
            continue
        try:
            versions[algo] = version(library)
        except PackageNotFoundError:
            print(f"skipping {algo}: {library} is not installed")
    return versions


class Evaluation:
    __slots__ = (
        "algorithms",
        "output_df",
        "results",
        "test_data",
        "versions",
    )

    def __init__(self, test_data: str, algorithms: list) -> None:
        self.test_data = self.read_data(test_data)
        self.versions = resolve_versions(algorithms)
        self.algorithms = list(self.versions)

    def run(self) -> None:
        """run the benchmark and write the results"""
        self.results = self.compute_results()
        self.output_df = self.create_df()
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.output_csv()
        self.output_md()
        self.print_scores()

    def read_data(self, path):
        """read test data set from a file path"""
        data = load_evaldata(path)
        if not isinstance(data, dict) or not data:
            raise ValueError(f"unrecognized test data format: {path}")
        validate(data)  # only handcrafted with/without chunks are supported
        return data

    def warm_up(self):
        "Pay the lazy imports and one-time constructors before timing starts."
        for a in self.algorithms:
            with suppress(Exception):  # an unimportable library is handled in compute_results
                ALGORITHMS[a]["function"](b"<html><body><p>text</p></body></html>")

    def compute_results(self):
        """run every algorithm over the test dataset and tally confusion matrices"""
        matrices = {a: BenchmarkMatrix() for a in self.algorithms}
        reported = set()  # algorithms whose first exception was printed
        disabled = set()  # installed but unimportable
        self.warm_up()
        i = 0
        for item in tqdm.tqdm(self.test_data.values()):
            htmlbinary = read_document(HERE, item["file"])
            if htmlbinary is None:
                print("HTML file not found:", item["file"])
                continue
            i += 1
            for a in self.algorithms:
                if a in disabled:
                    continue
                cm = matrices[a]
                result, counts, err = run_and_count(timed(ALGORITHMS[a]["function"], cm), htmlbinary, item)
                if isinstance(err, ImportError):
                    # drop it rather than publish an all-miss row
                    print(f"skipping {a}: {type(err).__name__}: {err}")
                    disabled.add(a)
                    continue
                if err is not None and a not in reported:
                    # ignored so the run continues; first failure per algorithm is still printed
                    reported.add(a)
                    print(f"{a}: {item['file']}: {type(err).__name__}: {err}")
                # empty output from a real library counts as a skip
                if not result and ALGORITHMS[a]["library"] != NO_LIBRARY:
                    cm.skipped += 1
                cm.add(counts)
        print(f"{i} from {len(self.test_data)} files read")
        if disabled:
            self.algorithms = [a for a in self.algorithms if a not in disabled]
            matrices = {a: cm for a, cm in matrices.items() if a not in disabled}
        return matrices

    def create_df(self):
        """results to pandas dataframe"""
        columns = ["algorithm", "version"] + METRICS + ["time difference", "skipped instances"]
        baseline_time = self.results["baseline"].time if "baseline" in self.results else 0.0
        rows = []
        for algo in self.algorithms:
            cm = self.results[algo]
            time_ratio = cm.time / baseline_time if baseline_time else 0.0
            rows.append([algo, self.versions[algo], *cm.scores(), time_ratio, cm.skipped])
        df = pd.DataFrame(rows, columns=columns)
        df.set_index("algorithm", inplace=True)
        return df.round(3)

    def output_csv(self, path="results.csv"):
        self.output_df.to_csv(os.path.join(OUTPUT_DIR, path))

    def output_md(self, path="results.md"):
        with open(os.path.join(OUTPUT_DIR, path), "w", encoding="utf-8") as f:
            f.write(self.output_df.to_markdown())

    def print_scores(self):
        """print results"""
        print("\n" + self.output_df.to_string())


def cmdparser():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run an evaluation benchmark")
    parser.add_argument("--small", action="store_true", help="Evaluate trafilatura and baselines only.")
    parser.add_argument("--all", action="store_true", help="Evaluate all available algorithms.")
    parser.add_argument("--testfile", default=os.path.join(HERE, "evaldata.json"), help="File path to the test data.")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=["everything", "nothing", "baseline"],
        help=f"Algorithms to evaluate, implemented: {list(ALGORITHMS)}.",
    )
    parser.add_argument("--verbose", action="store_true", help="increase verbosity")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


if __name__ == "__main__":
    args = cmdparser()

    if not args.verbose:
        logging.basicConfig(level=logging.CRITICAL)

    algorithms = ["everything", "nothing", "baseline"]
    if args.small:
        algorithms += ["trafilatura fast", "trafilatura"]
    elif args.all:
        algorithms = list(ALGORITHMS)
    else:
        algorithms += args.algorithms
        algorithms = sorted(set(algorithms))

    Evaluation(test_data=args.testfile, algorithms=algorithms).run()
