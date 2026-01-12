# tests/test_scraper_local.py
# unit tests for local file scraping in Scraper class.
import unittest
from pathlib import Path

from wiki_scraper.scraper import Scraper
from wiki_scraper.article import Article
from wiki_scraper.exceptions import ArticleNotFound


class TestScraperLocal(unittest.TestCase):
    def setUp(self):
        # Resolve path to sample HTML shipped with the repo
        repo_root = Path(__file__).resolve().parent.parent
        self.sample_path = repo_root / "tests" / "sample_data" / "team_rocket.html"

    def test_scrape_from_file_success(self):
        scraper = Scraper(
            base_url=str(self.sample_path),
            phrase="Team Rocket",
            use_local_file=True
        )
        article = scraper.scrape()

        self.assertIsInstance(article, Article)
        self.assertEqual(article.phrase, "Team Rocket")
        self.assertIn("Team Rocket", article.html_content)

    def test_scrape_from_file_not_found(self):
        missing_file = self.sample_path.parent / "missing.html"
        scraper = Scraper(
            base_url=str(missing_file),
            phrase="Anything",
            use_local_file=True
        )

        with self.assertRaises(ArticleNotFound):
            scraper.scrape()


if __name__ == "__main__":
    unittest.main()
