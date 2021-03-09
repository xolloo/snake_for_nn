import os
from setuptools import setup, find_packages

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_requires():
    path = os.path.join(BASE_DIR,"requirements.txt")
    with open(path, "r") as require_file:
        packages = [
            package.strip()
            for package in require_file.read().strip().split("\n")
        ]
    return packages

setup(
    name="game",
    version="1.0",
    author="Dmitriy Amelchenko",
    author_email="d.a.amelchenko@outlook.com",
    packages=find_packages("str", exclude=["*test*"]),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=get_requires(),
    python_requires=">=3.7",
    zip_safe=False,
    classifires=["Development Status :: 5 Production/Stable"]
)