## How to contribute


If you value this software or depend on it for your product,
consider sponsoring it and contributing to its codebase.
Your support will help ensure the sustainability and growth of the project.

There are many ways to contribute:

  * Sponsor the project: Show your appreciation [on GitHub](https://github.com/sponsors/adbar) or [ko-fi.com](https://ko-fi.com/adbarbaresi).
  * Find bugs and submit bug reports: Help making Trafilatura an even more robust tool.
  * Write code: Fix bugs or add new features by writing [pull requests](https://docs.github.com/en/pull-requests) with a list of what you have done.
  * Improve the documentation: Write tutorials and guides, correct mistakes, or translate existing content.
  * Submit feature requests: Share your feedback and suggestions.


Here are some important resources:

  * [List of currently open issues](https://github.com/adbar/trafilatura/issues) (no pretension to exhaustivity!)
  * [How to contribute to open source](https://opensource.guide/how-to-contribute/)

A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in Trafilatura.


## Testing and evaluating the code

Here is how you can run the tests and code quality checks, these are the same checks CI runs. Pull requests will only be accepted if the changes are tested and if there are no errors.

```
pip install -e ".[dev]"
pytest
mypy
ruff check .
ruff format --check .
```

Notes:

- The `-e` matters: plain `pip install trafilatura[dev]` would install the PyPI release instead of your changes.
- A single test suite can be selected, for example `pytest tests/realworld_tests.py`.
- Drop `--check` to let `ruff format` fix the formatting in place.

If you work on text extraction, CI runs an evaluation quality gate: `python tests/eval_gate.py` fails if extraction quality regresses below the pinned scores, so run it locally before pushing. Checking that performance is equal or better on the benchmarks is useful as well.

See the [tests Readme](tests/README.rst) and the testing page in the documentation for more information.


For further questions you can use [GitHub issues](https://github.com/adbar/trafilatura/issues) and discussion pages, or [E-Mail](https://adrien.barbaresi.eu/).

Thanks,

Adrien
