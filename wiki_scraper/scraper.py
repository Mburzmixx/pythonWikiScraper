# Module containing implementation of class `Scraper`.
# This class is responsible for scraping content from an appropriate file or a web-page.
from wiki_scraper.article import Article


class Scraper:
    def __init__(self, base_url: str, phrase: str, use_local_file=False):
        self.base_url = base_url
        self.phrase = phrase
        self.use_local_file = use_local_file

    def scrape(self) -> Article:
        pass
