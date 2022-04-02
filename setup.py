"""Setup the package."""

from setuptools import find_packages, setup

install_requires = [
    "numpy",
    "pandas<=1.3.5",
    "tqdm",
    "scipy",
    "scikit-learn",
    "pyTigerDriver==1.0.14",
    "pyTigerGraph==0.0.9.9.2",
    "tabulate",
    "pystow",
    "six",
]


setup_requires = ["pytest-runner"]

tests_require = ["pytest", "pytest-cov"]

extras_require = {
    "tests": tests_require,
    "docs": [
        "sphinx",
        "sphinx-rtd-theme",
        "sphinx-click",
        "sphinx-autodoc-typehints",
        "sphinx_automodapi",
        "nbsphinx_link",
        "jupyter-sphinx",
    ],
}

keywords = [
    "drug-combination",
    "drug-interaction",
]


setup(
    name="tigerlily",
    packages=find_packages(),
    version="0.1.0",
    license="Apache License, Version 2.0",
    description="TigerLily: Finding drug interactions in-silico with the Graph.",
    author="Benedek Rozemberczki",
    author_email="benedek.rozemberczki@gmail.com",
    url="https://github.com/benedekrozemberczki/tigerlily",
    download_url="https://github.com/benedekrozemberczki/tigerlily/archive/v0.1.0.tar.gz",
    keywords=keywords,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
