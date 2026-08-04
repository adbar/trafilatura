"""
Make extraction results comparable with other libraries of the same kind.
"""

import argparse
import logging
import os
import sys
import time

from dataclasses import dataclass
from functools import cache, partial
from importlib.metadata import PackageNotFoundError, version

import justext
import pandas as pd

from eval_common import (
    EXTRACT_OPTS,
    METRICS,
    RUNNERS,
    ConfusionMatrix,
    load_evaldata,
    read_corpus,
    report_first_error,
    run_and_count,
    validate,
)

from trafilatura import baseline, extract, html2txt
from trafilatura.external import jt_stoplist_init

# for run_custom
from justext.core import ParagraphMaker, classify_paragraphs, revise_paragraph_classification
from trafilatura.baseline import basic_cleaning
from trafilatura.utils import decode_file, load_html


# Competitors are imported in their runner, so a missing one only disables its own
# algorithm (see resolve_versions). justext is a Trafilatura dependency, always there.

JT_STOPLIST = jt_stoplist_init()

HERE = os.path.abspath(os.path.dirname(__file__))


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

    return Document(decode_file(htmlbinary)).summary()


def run_inscriptis(htmlbinary):
    """try with the inscriptis module"""
    from inscriptis import get_text

    return get_text(decode_file(htmlbinary))


def run_html2text(htmlbinary):
    """try with the html2text module"""
    import html2text

    return html2text.html2text(decode_file(htmlbinary))


def run_html_text(htmlbinary):
    """try with the html_text module"""
    import html_text

    return html_text.extract_text(decode_file(htmlbinary), guess_layout=False)


def run_boilerpipe(htmlbinary):
    """try with the boilerpipe algorithm"""
    return get_boilerpipe().get_content(decode_file(htmlbinary))


def run_newspaper(htmlbinary):
    """try with the newspaper package"""
    from newspaper import fulltext

    return fulltext(htmlbinary)


def run_newsplease(htmlbinary):
    """try with newsplease"""
    from newsplease import NewsPlease

    # fetch_images=False: the default fetches images from each article's live host
    return NewsPlease.from_html(decode_file(htmlbinary), url=None, fetch_images=False).maintext


def run_resiliparse(htmlbinary):
    """try with the resiliparse package"""
    from resiliparse.extract.html2text import extract_plain_text
    from resiliparse.parse.encoding import bytes_to_str, detect_encoding
    from resiliparse.parse.html import HTMLTree

    tree = HTMLTree.parse(bytes_to_str(htmlbinary, detect_encoding(htmlbinary)))
    return extract_plain_text(tree, main_content=True)


def run_bs4(htmlbinary):
    """try with the BeautifulSoup module"""
    from bs4 import BeautifulSoup

    # without a separator, gold chunks spanning an element boundary can never match
    return BeautifulSoup(htmlbinary, features="lxml").get_text(separator=" ", strip=True)


def run_magic_html(htmlbinary):
    """try with the magic_html package"""
    return run_bs4(get_magic_html().extract(decode_file(htmlbinary), base_url="").get("html"))


@dataclass
class BenchmarkMatrix(ConfusionMatrix):
    "Shared confusion matrix plus per-algorithm timing, skip and error bookkeeping."

    time: float = 0.0
    skipped: int = 0
    errors: int = 0


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

# algorithm string, package, function, results
ALGORITHMS = {
    "everything": {"library": NO_LIBRARY, "function": decode_file},
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
    def __init__(self, test_data: str, algorithms: list) -> None:
        self.test_data = load_evaldata(test_data)
        validate(self.test_data)  # only handcrafted with/without chunks are supported
        self.versions = resolve_versions(algorithms)

    def run(self) -> None:
        """run the benchmark and write the results"""
        df = self.create_df(self.compute_results())
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_csv(os.path.join(OUTPUT_DIR, "results.csv"))
        with open(os.path.join(OUTPUT_DIR, "results.md"), "w", encoding="utf-8") as f:
            f.write(df.to_markdown())
        print("\n" + df.to_string())

    def warm_up(self):
        """Pay the lazy imports and one-time constructors before timing starts;
        an unimportable library disables its algorithm rather than publish an all-miss row."""
        for a in list(self.versions):
            try:
                ALGORITHMS[a]["function"](b"<html><body><p>text</p></body></html>")
            except ImportError as err:
                print(f"skipping {a}: {type(err).__name__}: {err}")
                del self.versions[a]
            except Exception:  # other failures are reported per document in compute_results
                pass

    def compute_results(self):
        """run every algorithm over the test dataset and tally confusion matrices"""
        self.warm_up()
        docs = read_corpus(HERE, self.test_data)
        matrices = {a: BenchmarkMatrix() for a in self.versions}
        wrapped = {a: timed(ALGORITHMS[a]["function"], matrices[a]) for a in self.versions}
        reported = set()  # algorithms whose first exception was printed
        for i, (url, item) in enumerate(self.test_data.items(), 1):
            if i % 100 == 0:
                print(f"{i}/{len(self.test_data)} documents")
            htmlbinary = docs[url][1]
            for a, cm in matrices.items():
                result, counts, err = run_and_count(wrapped[a], htmlbinary, item)
                if err is not None:
                    # ignored so the run continues; the total makes a partly broken setup visible
                    cm.errors += 1
                    report_first_error(reported, a, item["file"], err)
                # empty output from a real library counts as a skip
                if not result and ALGORITHMS[a]["library"] != NO_LIBRARY:
                    cm.skipped += 1
                cm.add(counts)
        return matrices

    def create_df(self, results):
        """results to pandas dataframe"""
        columns = ["algorithm", "version"] + METRICS + ["time difference", "skipped instances", "errors"]
        baseline_time = results["baseline"].time if "baseline" in results else 0.0
        rows = []
        for algo, cm in results.items():
            time_ratio = cm.time / baseline_time if baseline_time else 0.0
            rows.append([algo, self.versions[algo], *cm.scores(), time_ratio, cm.skipped, cm.errors])
        df = pd.DataFrame(rows, columns=columns)
        df.set_index("algorithm", inplace=True)
        return df.round(3)


# always included: the ceiling rows and the timing reference
DEFAULT_ALGORITHMS = ["everything", "nothing", "baseline"]


def cmdparser():
    """Parse command line arguments and resolve the algorithm selection"""
    parser = argparse.ArgumentParser(description="Run an evaluation benchmark")
    parser.add_argument("--small", action="store_true", help="Evaluate trafilatura and baselines only.")
    parser.add_argument("--all", action="store_true", help="Evaluate all available algorithms.")
    parser.add_argument("--testfile", default=os.path.join(HERE, "evaldata.json"), help="File path to the test data.")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        choices=list(ALGORITHMS),
        metavar="ALGORITHM",
        default=[],
        help=f"Algorithms to evaluate, implemented: {list(ALGORITHMS)}.",
    )
    parser.add_argument("--verbose", action="store_true", help="increase verbosity")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.small:
        args.algorithms = DEFAULT_ALGORITHMS + ["trafilatura fast", "trafilatura"]
    elif args.all:
        args.algorithms = list(ALGORITHMS)
    else:
        args.algorithms = sorted(set(DEFAULT_ALGORITHMS + args.algorithms))
    return args


if __name__ == "__main__":
    args = cmdparser()

    if not args.verbose:
        logging.basicConfig(level=logging.CRITICAL)

    Evaluation(test_data=args.testfile, algorithms=args.algorithms).run()
