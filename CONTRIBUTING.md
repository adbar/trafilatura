# How to contribute


If you value this software or depend on it for your product,
consider sponsoring it and contributing to its codebase.
Your support will help ensure the sustainability and growth of the project.

There are many ways to contribute:

  * Sponsor the project: Show your appreciation [on GitHub](https://github.com/sponsors/adbar) or [ko-fi.com](https://ko-fi.com/adbarbaresi).
  * Find bugs and submit bug reports: Help make Trafilatura an even more robust tool.
  * Write code: Fix bugs or add new features by writing [pull requests](https://docs.github.com/en/pull-requests).
  * Improve the documentation: Write tutorials and guides or correct mistakes.
  * Submit feature requests: Share your feedback and suggestions.


Here are some important resources:

  * [List of currently open issues](https://github.com/adbar/trafilatura/issues) (not exhaustive!)
  * [How to contribute to open source](https://opensource.guide/how-to-contribute/)

A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in Trafilatura.


## Issues and pull requests

Search the open issues and pull requests first, someone may already be working on it.

Contributions are welcome on output formats, HTML elements, discovery (feeds, sitemaps, crawling), downloads and network, Unicode handling and the API.

Text extraction internals are maintained more closely: main content selection, fallback extractors, and heuristics. Open an issue and wait for an answer before writing code. These pull requests must report benchmark results.

One pull request per issue. The first complete one with tests is merged, later ones only if substantially better.

Keep pull requests short. A bug fix is the smallest change that fixes the bug. Reuse existing helpers in Trafilatura and its dependencies, such as courlan, before writing new code. No new dependencies. Do not edit HISTORY.md.

Add tests for the changed behavior, ideally one that fails before the change. Test through the public functions, not internals. Group similar cases with `pytest.mark.parametrize` instead of writing one test per case.

Changes that run on every extraction report the processing time before and after.

Pull requests are squash-merged, so only the title needs to follow [Conventional Commits](https://www.conventionalcommits.org/), for example `fix(sitemaps): ...` or `feat(cli): ...`, where the part in brackets is the module or area concerned.

Rebase on master when your pull request conflicts with it. Conflicting pull requests are not reviewed. Pull requests are reviewed oldest first, up to 3 per author at a time.


## Using AI tools

AI tools are welcome. The same rules apply as for any other contribution, plus the following:

  * You are the author. Review, understand and test every line before asking for a review. Write the description and your replies to reviews yourself, translation and grammar tools are fine.
  * No autonomous agents. A human approves every issue, pull request and comment before it is posted.
  * Disclosure is appreciated: name the tool and what it was used for in the pull request description.
  * Every commit needs a human author. AI trailers such as `Co-Authored-By` or `Assisted-by` can be added next to it.
  * You must have the right to submit your whole contribution under the [Apache 2.0 license](LICENSE).

A contribution should be worth more to the project than the time it takes to review it. Pull requests that do not follow these rules are closed with a short reason.

Instructions for coding agents are in [AGENTS.md](AGENTS.md).


## Testing and evaluating the code

Here is how you can run the tests and code quality checks, these are the same checks CI runs. Pull requests will only be accepted if the changes are tested and if there are no errors.

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
- The `all` extra matches the CI environment of the quality gate. With `".[dev]"` only, gate scores can differ slightly on non-UTF-8 pages.
- A single test suite can be selected, for example `pytest tests/realworld_tests.py`.
- Drop `--check` to let `ruff format` fix the formatting in place.
- The documentation tests need the docs extra, which requires Python 3.12 or later: `uv pip install -e ".[docs]"` then `pytest docs/docs_tests.py`.

The evaluation quality gate `python tests/eval_gate.py` fails if extraction quality regresses below the pinned scores. CI runs it on every pull request. If you work on text extraction, also report scores before and after on these benchmarks, using the evaluation tool each one provides:

- [AEB](https://github.com/scrapinghub/article-extraction-benchmark), article extraction benchmark (articles only).
- [WCXB](https://github.com/Murrough-Foley/web-content-extraction-benchmark), web content extraction benchmark (7 page types), on the `test` split.
- [WMB](https://github.com/opendatalab/WebMainBench), WebMainBench.

For processing time, run `python tests/evaluate.py --small` on master and on your branch, it needs the `eval` extra and Python 3.11+. The "time difference" column is relative to the baseline extractor.

See the [tests Readme](tests/README.rst) and the [testing page](https://trafilatura.readthedocs.io/en/latest/tests.html) in the documentation for more information.


For further questions you can use [GitHub issues](https://github.com/adbar/trafilatura/issues) and discussion pages, or [E-Mail](https://adrien.barbaresi.eu/).

Thanks,

Adrien
