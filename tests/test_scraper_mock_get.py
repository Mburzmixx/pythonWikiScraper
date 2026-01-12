# tests/test_scraper_mock_get.py
# unit tests where requests.get is mocked to avoid real HTTP requests.
from unittest.mock import patch, Mock
import unittest

from wiki_scraper.scraper import Scraper
from wiki_scraper.article import Article
from wiki_scraper.exceptions import ArticleNotFound


class TestScraperMockGet(unittest.TestCase):
    @patch("wiki_scraper.scraper.requests.get")
    def test_scrape_from_web_success(self, mock_get):
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <body>
                    <div class='mw-content-ltr mw-parser-output'>
                        <p> Test paragraph -- Generations. </p>
                    </div>
                </body>
            </html>
            """
        mock_get.return_value = mock_response

        scraper = Scraper(
            base_url="https://bulbapedia.bulbagarden.net/wiki/",
            phrase="Generation",
            use_local_file=False
        )

        article = scraper.scrape()

        self.assertIsInstance(article, Article)
        self.assertEqual(article.phrase, "Generation")
        self.assertIn("Test paragraph -- Generations.", article.html_content)

        estimated_headers = {
            "User-Agent": (
                "wiki_scraper_bot/1.0 "
                "(contact: mburza@student.uw.edu.pl)"
            )
        }

        estimated_timeout = 10

        mock_get.assert_called_once_with(
            "https://bulbapedia.bulbagarden.net/wiki/Generation",
            headers=estimated_headers,
            timeout=estimated_timeout
        )


if __name__ == "__main__":
    unittest.main()
