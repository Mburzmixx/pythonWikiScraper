# Module containing implementation of class `Article`.
# This class is responsible for parsing scrapped content.
import pandas as pd


class Article:
    def __init__(self, html_content, phrase):
        self.html_content = html_content
        self.phrase = phrase

    def get_first_paragraph(self):
        pass

    def get_table_by_index(self, index: int) -> pd.DataFrame:
        pass

    def count_words(self) -> dict[str, int]:
        pass
