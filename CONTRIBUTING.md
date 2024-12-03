## How to contribute

Your contributions make the software and its documentation better. A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in Trafilatura.


There are many ways to contribute, you could:

  * Improve the documentation: Write tutorials and guides, correct mistakes, or translate existing content.
  * Find bugs and submit bug reports: Help making Trafilatura an even more robust tool.
  * Submit feature requests: Share your feedback and suggestions.
  * Write code: Fix bugs or add new features.


Here are some important resources:

  * [List of currently open issues](https://github.com/adbar/trafilatura/issues) (no pretention to exhaustivity!)
  * [How to contribute to open source](https://opensource.guide/how-to-contribute/)


## Testing and evaluating the code

Here is how you can run the tests and code quality checks:

- Install the necessary packages with `pip install trafilatura[dev]`
- Run `pytest` from trafilatura's directory, or select a particular test suite, for example `realworld_tests.py`, and run `pytest realworld_tests.py` or simply `python3 realworld_tests.py`
- Run `mypy` on the directory: `mypy trafilatura/`
- See also the [tests Readme](tests/README.rst) for information on the evaluation benchmark

Pull requests will only be accepted if they there are no errors in pytest and mypy.

If you work on text extraction it is useful to check if performance is equal or better on the benchmark.


## Submitting changes

Please send a pull request to Trafilatura with a list of what you have done (read more about [pull requests](http://help.github.com/pull-requests/)).

**Working on your first Pull Request?** See this tutorial: [How To Create a Pull Request on GitHub](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github)



For further questions you can use [GitHub issues](https://github.com/adbar/trafilatura/issues) and discussion pages, or [E-Mail](https://adrien.barbaresi.eu/).

Thanks,

Adrien
