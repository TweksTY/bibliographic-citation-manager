import tempfile
from pathlib import Path

import utils.database as db
from utils.citation_types import Author, Book


def _open_db(tmp_path: Path):
    db_path = tmp_path / "test_citations.db"
    conn = db.create_connection(str(db_path))
    assert conn is not None
    db.create_table(conn)
    return conn


def test_insert_and_fetch_book(tmp_path):
    conn = _open_db(tmp_path)
    try:
        book = Book(
            {
                "title": "Programming Basics",
                "language": "en",
                "city": "Kyiv",
                "year": 2020,
                "pages_count": 250,
                "publisher": "Nauka",
                "publishing_number": None,
                "publishing_type": "textbook",
                "authors": [Author("Ivan", "Petrenko", "Mykolayovych")],
            }
        )
        entry_id = db.insert_entry(conn, book)
        assert entry_id is not None

        entries = db.get_entries(conn, sort_by="title")
        assert len(entries) == 1
        saved = entries[0]
        assert saved.title == "Programming Basics"
        assert saved.publisher == "Nauka"
        assert saved.type == "Book"
        assert len(saved.authors) == 1
        assert saved.authors[0].last_name == "Petrenko"

        db.delete_entry(conn, saved.id)
        assert db.get_entries(conn) == []
    finally:
        conn.close()


def test_author_reuse_across_entries(tmp_path):
    conn = _open_db(tmp_path)
    try:
        first = Book(
            {
                "title": "Book One",
                "language": "en",
                "city": "Kyiv",
                "year": 2019,
                "pages_count": 100,
                "publisher": "Nauka",
                "publishing_number": None,
                "publishing_type": None,
                "authors": [Author("Anna", "Shevchenko", None)],
            }
        )
        second = Book(
            {
                "title": "Book Two",
                "language": "en",
                "city": "Lviv",
                "year": 2021,
                "pages_count": 120,
                "publisher": "Osnova",
                "publishing_number": None,
                "publishing_type": None,
                "authors": [Author("Anna", "Shevchenko", None)],
            }
        )
        db.insert_entry(conn, first)
        db.insert_entry(conn, second)

        authors = db.get_authors(conn)
        assert len(authors) == 1
        assert authors[0].first_name == "Anna"
        assert len(db.get_entries(conn)) == 2
    finally:
        conn.close()
