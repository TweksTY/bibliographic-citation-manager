from utils.citation_types import Author, Book


class TestAuthor:
    def test_abbr_name_simple(self):
        assert Author("Ivan", "Petrenko", None).get_abbr_name() == "I."

    def test_abbr_name_hyphenated(self):
        assert Author("Jean-Luc", "Picard", None).get_abbr_name() == "J.-L."

    def test_is_empty(self):
        assert Author("", "", None).is_empty()
        assert not Author("Anna", "Shevchenko", None).is_empty()

    def test_to_dict(self):
        author = Author("Ivan", "Petrenko", "Mykolayovych")
        assert author.to_dict() == {
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "middle_name": "Mykolayovych",
        }


class TestBookCitations:
    def test_dstu_2015(self, sample_book):
        assert sample_book.get_DSTU2015_citation() == (
            "Petrenko I. M. Programming Basics : textbook. "
            "Kyiv : Nauka, 2020. 250 p."
        )

    def test_dstu_2006(self, sample_book):
        assert sample_book.get_DSTU2006_citation() == (
            "Petrenko I. M. Programming Basics : textbook /  "
            "Ivan Mykolayovych Petrenko. — Kyiv : Nauka, 2020. — 250 p."
        )

    def test_apa(self, sample_book):
        assert sample_book.get_APA_citation() == (
            "Petrenko, I. M. (2020). Programming Basics. Nauka."
        )

    def test_mla(self, sample_book):
        assert sample_book.get_MLA_citation() == (
            "Petrenko, Ivan Mykolayovych  Programming Basics. Nauka, 2020."
        )

    def test_ukrainian_dstu_2015(self):
        book = Book(
            {
                "title": "Основи програмування",
                "language": "uk",
                "city": "Київ",
                "year": 2020,
                "pages_count": 250,
                "publisher": "Наука",
                "publishing_type": "підручник",
                "authors": [Author("Іван", "Петренко", "Миколайович")],
            }
        )
        citation = book.get_DSTU2015_citation()
        assert citation.startswith("Петренко І. М.")
        assert "Основи програмування : підручник." in citation
        assert "Київ : Наука, 2020. 250 с." in citation
