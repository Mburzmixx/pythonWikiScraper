# Module containing implementation of class `Article`.
# This class represents an article
# and is responsible for parsing scrapped content.
from bs4 import BeautifulSoup
from pandas import DataFrame


class Article:
    def __init__(self, html_content, phrase: str):
        self.html_content = html_content
        self.phrase = phrase
        self._parsed_content = BeautifulSoup(self.html_content, "html.parser")

    def get_first_paragraph(self) -> str:
        container = self._parsed_content.find(
            "div", class_="mw-content-ltr mw-parser-output"
        )

        if container is not None:
            paragraph = container.find("p")
            if paragraph is not None:
                return paragraph.get_text(strip=True)
        return ""

    def get_table_by_index(self, index: int) -> DataFrame:
        raise NotImplementedError()

    def count_words(self) -> dict[str, int]:
        raise NotImplementedError()
