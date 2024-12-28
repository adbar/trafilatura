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

  * [List of currently open issues](https://github.com/adbar/trafilatura/issues) (no pretention to exhaustivity!)
  * [How to contribute to open source](https://opensource.guide/how-to-contribute/)

A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in Trafilatura.


## Testing and evaluating the code

Here is how you can run the tests and code quality checks. Pull requests will only be accepted if the changes are tested and if they there are no errors. 

- Install the necessary packages with `pip install trafilatura[dev]`
- Run `pytest` from trafilatura's directory, or select a particular test suite, for example `realworld_tests.py`, and run `pytest realworld_tests.py` or simply `python3 realworld_tests.py`
- Run `mypy` on the directory: `mypy trafilatura/`

If you work on text extraction it is useful to check if performance is equal or better on the benchmark.

See the [tests Readme](tests/README.rst) for more information.


For further questions you can use [GitHub issues](https://github.com/adbar/trafilatura/issues) and discussion pages, or [E-Mail](https://adrien.barbaresi.eu/).

Thanks,

Adrien
