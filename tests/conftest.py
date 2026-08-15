"""Shared fixtures for unit tests."""

import pytest

from utils.citation_types import Author, Book, Article, Site


@pytest.fixture
def single_author():
    return Author("Ivan", "Petrenko", "Mykolayovych")


@pytest.fixture
def sample_book(single_author):
    return Book(
        {
            "title": "Programming Basics",
            "language": "en",
            "city": "Kyiv",
            "year": 2020,
            "pages_count": 250,
            "publisher": "Nauka",
            "publishing_type": "textbook",
            "authors": [single_author],
        }
    )


@pytest.fixture
def sample_article():
    return Article(
        {
            "title": "Machine Learning Survey",
            "language": "en",
            "year": 2021,
            "journal": "CS Journal",
            "issue": 3,
            "number": 12,
            "pages_cited": "10-25",
            "authors": [
                Author("Anna", "Shevchenko", None),
                Author("Oleg", "Kovalenko", "Petrovych"),
            ],
            "url": "https://example.com/article",
            "access_date": "2024-01-15",
        }
    )


@pytest.fixture
def sample_site():
    return Site(
        {
            "title": "Python Docs",
            "language": "en",
            "year": 2023,
            "url": "https://docs.python.org",
            "access_date": "2024-05-01",
            "publisher": "PSF",
            "authors": [],
        }
    )
