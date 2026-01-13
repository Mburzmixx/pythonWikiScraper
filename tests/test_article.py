# tests/test_article_reading_words.py
# Unit tests for class `Article`:
# 1. focused on checking how it reads words,
# 2.
import unittest
from pathlib import Path
from wiki_scraper.article import Article

from wiki_scraper.scraper import Scraper


class TestArticleWordReading(unittest.TestCase):
    def setUp(self):
        # Resolve path to sample HTML shipped with the repo
        repo_root = Path(__file__).resolve().parent.parent
        self.simple_path = [repo_root / "tests" / "sample_data" /
                            f"simple_article_{i}.html" for i in range(4)]

    def test_empty_article_mock(self):
        article = Article("", "")

        expected_str = ""
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_empty_article_locally(self):
        scraper = Scraper(
            base_url=str(self.simple_path[0]),
            phrase="Test0",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = ""
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_reading_first_paragraph_easy(self):
        scraper = Scraper(
            base_url=str(self.simple_path[1]),
            phrase="Test1",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = "This is the first paragraph. It contains some text for testing."
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)

    def test_reading_first_paragraph_sep(self):
        scraper = Scraper(
            base_url=str(self.simple_path[2]),
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
            base_url=str(self.simple_path[3]),
            phrase="Test3",
            use_local_file=True
        )
        article = scraper.scrape()

        expected_str = ""
        actual_str = article.get_first_paragraph()

        self.assertEqual(expected_str, actual_str)


class TestArticleReadingTables(unittest.TestCase):
    def setUp(self):
        # Resolve path to sample HTML shipped with the repo
        repo_root = Path(__file__).resolve().parent.parent
        self.simple_path = [repo_root / "tests" / "sample_data" /
                            f"table_simple_{i}.html" for i in range(4)]

        self.mid_path = [repo_root / "tests" / "sample_data" /
                         f"table_mid_{i}.html" for i in range(1)]

    def test_simple_table(self):
        scraper = Scraper(
            base_url=str(self.simple_path[0]),
            phrase="Test0",
            use_local_file=True
        )
        article = scraper.scrape()
        df = article.get_table_by_index(1)

        self.assertEqual(df.shape, (3, 3))
        self.assertIn("Type", df.columns)
        self.assertIn("Color", df.columns)
        self.assertIn("Example", df.columns)

        self.assertEqual(df.iloc[0, 0], "Fire")
        self.assertEqual(df.iloc[1, 0], "Water")
        self.assertEqual(df.iloc[2, 0], "Grass")

    def test_table_index_not_one(self):
        scraper = Scraper(
            base_url=str(self.simple_path[1]),
            phrase="Test1",
            use_local_file=True
        )
        article = scraper.scrape()
        df = article.get_table_by_index(2)

        self.assertEqual(df.shape, (2, 3))
        self.assertIn("Generation", df.columns)

    def test_bigger_table(self):
        scraper = Scraper(
            base_url=str(self.simple_path[2]),
            phrase="Test2",
            use_local_file=True
        )
        article = scraper.scrape()
        df = article.get_table_by_index(1)

        self.assertEqual(df.shape, (3, 4))
        self.assertIn("Super Effective Against", df.columns)

        self.assertEqual(df.iloc[0, 0], "Fire")
        self.assertIn("Grass", df.iloc[0, 1])

    def test_no_tables(self):
        scraper = Scraper(
            base_url=str(self.simple_path[3]),
            phrase="Test3",
            use_local_file=True
        )
        article = scraper.scrape()
        df = article.get_table_by_index(1)

        self.assertTrue(df.empty)

    def test_detection_of_headers(self):
        scraper = Scraper(
            base_url=str(self.mid_path[0]),
            phrase="Test4",
            use_local_file=True
        )
        article = scraper.scrape()
        df = article.get_table_by_index(1)

        self.assertEqual(df.shape, (6, 2))
        self.assertIn("Type effectiveness", df.columns)
        self.assertIn("Multiplier", df.columns)

        self.assertEqual(df.iloc[0, 0], "Doubly super effective")
        self.assertEqual(df.iloc[0, 1], "×2.56")

        self.assertIn("Triply resisted", df.iloc[5, 0])
        self.assertEqual(df.iloc[5, 1], "×0.244140625")


if __name__ == "__main__":
    unittest.main()
