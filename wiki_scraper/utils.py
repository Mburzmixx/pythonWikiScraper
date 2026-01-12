# Module containing utility stuff.
import pandas as pd
import time
from pathlib import Path

OK = 0
BULBAPEDIA_URL = "abecadle"
dict_path = Path("word-counts.json")


def update_word_counts(to_add: dict[str, int]):
    raise NotImplementedError()


def analyze_relative_word_freq(mode: str, n: int, chart_path=None):
    raise NotImplementedError()


def get_relative_freq_table() -> pd.DataFrame:
    raise NotImplementedError()


def auto_count_words(start_phrase: str, depth: int, wait: float):
    raise NotImplementedError()
