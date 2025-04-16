from setuptools import setup, find_packages
from loaders import __version__


with open('requirements.txt', encoding="utf-8") as f:
    required = f.read().splitlines()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="armenian_news_scraper",
    version=__version__,
    description="Scraper and summarizer for Armenian government news sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tigran Margaryan",
    packages=find_packages(include=['loaders', 'loaders.*']),

    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
