[pypi-image]: https://badge.fury.io/py/tigerlily.svg
[pypi-url]: https://pypi.python.org/pypi/tigerlily
[size-image]: https://img.shields.io/github/repo-size/benedekrozemberczki/tigerlily.svg
[size-url]: https://github.com/benedekrozemberczki/tigerlily/archive/main.zip
[build-image]: https://github.com/benedekrozemberczki/tigerlily/workflows/CI/badge.svg
[build-url]: https://github.com/benedekrozemberczki/tigerlily/actions?query=workflow%3ACI
[docs-image]: https://readthedocs.org/projects/tigerlily/badge/?version=latest
[docs-url]: https://tigerlily.readthedocs.io/en/latest/?badge=latest
[coverage-image]: https://codecov.io/gh/benedekrozemberczki/tigerlily/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/github/benedekrozemberczki/tigerlily?branch=main


--------------------------------------------------------------------------------

[![PyPI Version][pypi-image]][pypi-url]
[![Docs Status][docs-image]][docs-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Build Status][build-image]][build-url]

**[Documentation](https://tigerlily.readthedocs.io)** | **[Example](https://github.com/benedekrozemberczki/tigerlily/tree/main/examples)** 

<p align="center">
  <img width="100%" src="https://github.com/benedekrozemberczki/tigerlily/blob/main/images/tigerlily_logo.jpg?sanitize=true" />
</p>


*tigerlily* is a .....

--------------------------------------------------------------------------------

**Drug Interaction Prediction with Tigerlily**

Our framework solves the [drug pair scoring task](https://arxiv.org/abs/2111.02916) . In this machine learning task ..



<p align="center">
  <img width="90%" src="https://github.com/benedekrozemberczki/tigerlily/blob/main/images/pair_scoring.jpg?sanitize=true" />
</p>


**Getting Started**

The API of `tigerlily` ....


```python
from tigerlily import ...
```

Head over to our [documentation](https://tigerlily.readthedocs.io) to find out more about installation, creation of datasets and a full list of implemented methods and available datasets.
For a quick start, check out the `examples/` directory.

If you notice anything unexpected, please open an [issue](github.com/benedekrozemberczki/tigerlily/issues). If you are missing a specific method, feel free to open a [feature request](https://github.com/benedekrozemberczki/tigerlily/issues).


--------------------------------------------------------------------------------

**Citing**


If you find *Tigerlily* useful in your research, please consider adding the following citation:

```bibtex
@misc{tigerlily2022,
  author = {Benedek Rozemberczki},
  title = {TigerLily: Finding drug interactions in-silico with the Graph},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/benedekrozemberczki/tigerlily}},
}
```

--------------------------------------------------------------------------------

**Installation**

To install tigerlily, simply run

```sh
pip install tigerlily
```

**Running tests**

```
$ tox -e py
```
--------------------------------------------------------------------------------

**License**

- [Apache 2.0 License](https://github.com/benedekrozemberczki/tigerlily/blob/main/LICENSE)
