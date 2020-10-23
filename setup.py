import io
import os
import re

from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", os.linesep)
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_version():
    content = read(os.path.join(os.path.dirname(__file__), "hijet", "__init__.py"))
    return re.search(r"__version__ = \"([^']+)\"\n", content).group(1)


setup(
    name="hijet",
    version=read_version(),
    packages=find_packages(),
    license="MIT",
    author="minazukie",
    url="https://github.com/minazukie/hijet",
    author_email="minazukie2015@gmail.com",
    description="Multiple Jetbrains IDEs, One Command",
    install_requires=[],
    test_suite=None,
    tests_require=[],
    entry_points={"console_scripts": ["hijet = hijet.main:main"]},
)
