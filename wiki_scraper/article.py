# Module containing implementation of class `Article`.
# This class represents an article
# and is responsible for parsing scrapped content.
from bs4 import BeautifulSoup
import pandas as pd


class Article:
    def __init__(self, html_content, phrase):
        self.html_content = html_content
        self.phrase = phrase
        self._parsed_content = BeautifulSoup(self.html_content, "html.parser")

    def get_first_paragraph(self):
        pass

    def get_table_by_index(self, index: int) -> pd.DataFrame:
        pass

    def count_words(self) -> dict[str, int]:
        pass
