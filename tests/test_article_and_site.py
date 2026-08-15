class TestArticleCitations:
    def test_dstu_2015(self, sample_article):
        assert sample_article.get_DSTU2015_citation() == (
            "Shevchenko A., Kovalenko O. P. Machine Learning Survey. "
            "CS Journal. Vol. 12, № 3. P. 10-25. "
            "URL: https://example.com/article (date of access: 2024-01-15)."
        )

    def test_apa(self, sample_article):
        assert sample_article.get_APA_citation() == (
            "Shevchenko, A.  & Kovalenko, O. P. (2021). "
            "Machine Learning Survey. CS Journal, 12(3), 10-25. "
            "https://example.com/article."
        )

    def test_mla(self, sample_article):
        assert sample_article.get_MLA_citation() == (
            'Shevchenko, Anna, and Oleg Petrovych Kovalenko.. '
            '"Machine Learning Survey". CS Journal, vol. 12, no. 3, 2021, '
            "p. 10-25. https://example.com/article. Accessed 2024-01-15."
        )


class TestSiteCitations:
    def test_apa_without_authors(self, sample_site):
        assert sample_site.get_APA_citation() == (
            "PSF Python Docs. (n.d.). Python Docs. "
            "Retrieved 2024-05-01 from https://docs.python.org."
        )

    def test_mla_without_authors(self, sample_site):
        assert sample_site.get_MLA_citation() == (
            '"Python Docs" PSF,  https://docs.python.org. Accessed 2024-05-01.'
        )

    def test_dstu_2015_without_authors(self, sample_site):
        assert sample_site.get_DSTU2015_citation() == (
            "Python Docs. PSF."
            " URL: https://docs.python.org (date of access: 2024-05-01)."
        )
