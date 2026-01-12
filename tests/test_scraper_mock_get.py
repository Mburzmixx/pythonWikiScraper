# tests/test_scraper_mock_get.py
# unit tests where requests.get is mocked to avoid real HTTP requests.
from unittest.mock import patch, Mock
import unittest

import requests

from wiki_scraper.scraper import Scraper
from wiki_scraper.article import Article
from wiki_scraper.exceptions import ArticleNotFound


class TestScraperMockGet(unittest.TestCase):
    @patch("wiki_scraper.scraper.requests.get")
    def test_scrape_from_web_success(self, mock_get):
        # Mock response object
        mock_200 = Mock()
        mock_200.status_code = 200
        mock_200.text = """
            <html>
                <body>
                    <div class='mw-content-ltr mw-parser-output'>
                        <p> Test paragraph -- Generations. </p>
                    </div>
                </body>
            </html>
            """
        mock_get.return_value = mock_200

        scraper = Scraper(
            base_url="https://bulbapedia.bulbagarden.net/wiki/",
            phrase="Generation",
            use_local_file=False
        )

        article = scraper.scrape()

        self.assertIsInstance(article, Article)
        self.assertEqual(article.phrase, "Generation")
        self.assertIn("Test paragraph -- Generations.", article.html_content)

        mock_get.assert_called_once_with(
            "https://bulbapedia.bulbagarden.net/wiki/Generation",
            headers=Scraper.headers,
            timeout=Scraper.requests_timeout
        )

    @patch("wiki_scraper.scraper.requests.get")
    def test_scrape_from_web_not_found(self, mock_get):
        # Mock response object for 404
        mock_404 = Mock()
        mock_404.status_code = 404
        mock_404.raise_for_status.side_effect = requests.HTTPError(
            "404 Client Error: Not Found for url"
        )
        mock_get.return_value = mock_404

        scraper = Scraper(
            base_url="https://bulbapedia.bulbagarden.net/wiki/",
            phrase="NonExistentArticle",
            use_local_file=False
        )

        with self.assertRaises(ArticleNotFound):
            scraper.scrape()

        self.assertEqual(mock_get.call_count, Scraper.num_attempts)

    @patch("wiki_scraper.scraper.time.sleep")
    @patch("wiki_scraper.scraper.requests.get")
    def test_scrape_from_web_retry(self, mock_get, mock_sleep):
        mock_429 = Mock()
        mock_429.status_code = 429
        mock_429.headers = {"Retry-After": "2"}

        mock_200 = Mock()
        mock_200.status_code = 200
        mock_200.text = """
            <html>
                <body>
                    <div class='mw-content-ltr mw-parser-output'>
                        <p> Test paragraph after retry. </p>
                    </div>
                </body>
            </html>
            """

        mock_get.side_effect = [mock_429, mock_429, mock_200]

        scraper = Scraper(
            base_url="https://bulbapedia.bulbagarden.net/wiki/",
            phrase="Generation",
            use_local_file=False
        )

        article = scraper.scrape()

        self.assertIsInstance(article, Article)
        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        self.assertEqual(article.phrase, "Generation")
        mock_get.assert_called_with(
            "https://bulbapedia.bulbagarden.net/wiki/Generation",
            headers=Scraper.headers,
            timeout=Scraper.requests_timeout
        )


if __name__ == "__main__":
    unittest.main()
