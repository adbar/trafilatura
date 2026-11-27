# How to contribute


Bug reports, feature requests, documentation and code are all welcome. If you value this software or depend on it for your product, consider sponsoring it [on GitHub](https://github.com/sponsors/adbar) or [ko-fi.com](https://ko-fi.com/adbarbaresi).

A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in Trafilatura.


## Issues and pull requests

Search the [open issues](https://github.com/adbar/trafilatura/issues) and pull requests first. Someone may already be working on it. One pull request per issue: the first complete one with tests is usually merged.

Contributions are welcome on output formats, HTML elements, discovery (feeds, sitemaps, crawling), downloads and network, Unicode handling and the API. Text extraction is maintained more closely (main content selection, fallback extractors and heuristics). For these changes, please open an issue first to discuss the approach.

Keep pull requests short. A bug fix is ideally the smallest change that fixes the bug. Reuse existing helpers, in Trafilatura or in dependencies such as courlan, and avoid new dependencies. There is no need to edit HISTORY.md. The maintainer updates it.

Add tests for the changed behavior, ideally one that fails before the change. Test through the public functions as far as possible. Similar cases can be grouped with `pytest.mark.parametrize`.

Pull requests are squash-merged, so only the title needs to follow [Conventional Commits](https://www.conventionalcommits.org/), for example `fix(sitemaps): ...` or `feat(cli): ...`. Please rebase on master if your pull request conflicts with it. Pull requests are reviewed oldest first, up to 3 per author at a time.


## Using AI tools

AI tools are welcome. The same rules apply as for any other contribution, plus the following:

  * You are the author. Review, understand and test every line before asking for a review.
  * Write the description and your replies to reviews yourself. Translation and grammar tools are fine.
  * No autonomous agents. A human approves every issue, pull request and comment before it is posted.
  * Disclosure is appreciated: name the tool and what it was used for in the pull request description.
  * Every commit needs a human author. AI trailers such as `Co-Authored-By` can be added next to it.
  * You must have the right to submit your whole contribution under the [Apache 2.0 license](LICENSE).

A contribution should be worth more to the project than the time it takes to review it. Pull requests that ignore these rules may be closed with a short reason.

Instructions for coding agents are in [AGENTS.md](AGENTS.md).


## Testing and evaluating the code

Pull requests are only accepted if CI passes and if they don't add gaps in test coverage. These are the checks CI runs:

```
uv venv && source .venv/bin/activate
uv pip install -e ".[dev,all]"
pytest
mypy
ruff check .
ruff format --check .
python tests/eval_gate.py
```

Notes:

- On Windows, activate the environment with `.venv\Scripts\activate`.
- The `-e` matters: a plain install would use the PyPI release instead of your changes.
- Drop `--check` to let `ruff format` fix the formatting in place.
- CI also runs the documentation tests. They need Python 3.12 or later: `uv pip install -e ".[docs]"` then `pytest docs/docs_tests.py`.
- CI tests Python 3.10 to 3.15 on Linux and 3.11 on macOS and Windows, mostly with `".[dev]"` only. Code has to run on Python 3.10 and without the optional dependencies of the `all` extra.
- Some tests in `tests/downloads_tests.py` need network access.
- Codecov measures coverage on Python 3.13 with the `all` extra. To check it locally: `pytest --cov=trafilatura --cov-report=term-missing`.

The quality gate `python tests/eval_gate.py` fails if extraction quality drops below the pinned scores. It runs on the annotated pages in `tests/evaldata.json` and checks two things:

- Text: the F1-score of the extracted text, compared with the floors in `tests/eval_baseline.json`
- Metadata: for title, author, date, tags and categories, the share of annotated values found by `extract_metadata`, compared with the floors in `tests/eval_meta_baseline.json`

If your change raises a score or edits the annotated pages, re-pin with `python tests/eval_gate.py --update` and commit the updated baseline. A re-pin never lowers a floor on its own.

If you work on text extraction, please report scores before and after on these benchmarks if possible, using the evaluation tool each one provides:

- [AEB](https://github.com/scrapinghub/article-extraction-benchmark), article extraction benchmark (articles only).
- [WCXB](https://github.com/Murrough-Foley/web-content-extraction-benchmark), web content extraction benchmark (7 page types), on the `test` split.
- [WMB](https://github.com/opendatalab/WebMainBench), WebMainBench.

For changes that run on every extraction, the processing time before and after is welcome too. Run `python tests/evaluate.py --small` on master and on your branch. It needs the `eval` extra and Python 3.11+. The "time difference" column is relative to the baseline extractor.

See the [tests Readme](tests/README.rst) and the [testing page](https://trafilatura.readthedocs.io/en/latest/tests.html) in the documentation for more information.


For further questions you can use [GitHub issues](https://github.com/adbar/trafilatura/issues) and discussion pages, or [E-Mail](https://adrien.barbaresi.eu/).

Thanks,

Adrien
