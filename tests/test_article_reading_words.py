# tests/test_article_reading_words.py
# unit tests for class article focused on checking
# if it reads words correctly
import unittest
from pathlib import Path
from wiki_scraper.article import Article

from wiki_scraper.scraper import Scraper


class TestArticleWordReading(unittest.TestCase):
    def setUp(self):
        # Resolve path to sample HTML shipped with the repo
        repo_root = Path(__file__).resolve().parent.parent
        self.sample_path = [repo_root / "tests" / "sample_data" /
                            f"simple_article_{i}.html" for i in range(4)]

    def test_empty_article_mock(self):
        article = Article("", "")

        expected_str = ""
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_empty_article_locally(self):
        scraper = Scraper(
            base_url=str(self.sample_path[0]),
            phrase="Test0",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = ""
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_reading_first_paragraph_easy(self):
        scraper = Scraper(
            base_url=str(self.sample_path[1]),
            phrase="Test1",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = "This is the first paragraph. It contains some text for testing."
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_reading_first_paragraph_sep(self):
        scraper = Scraper(
            base_url=str(self.sample_path[2]),
            phrase="Test2",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = ("This is the first paragraph. It contains some text for testing. "
                        "This time it is tricky")
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_article_without_paragraphs(self):
        scraper = Scraper(
            base_url=str(self.sample_path[3]),
            phrase="Test3",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = ""
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)


if __name__ == "__main__":
    unittest.main()
