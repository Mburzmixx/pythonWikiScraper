# Module containing utility stuff.
from json import load, dump
from wordfreq import word_frequency, top_n_list
from pandas import DataFrame
import time
import matplotlib.pyplot as plt
from pathlib import Path

OK = 0
BULBAPEDIA_URL = "abecadle"
repo_root = Path(__file__).resolve().parent.parent
dict_path = repo_root / "wiki_scraper" / "word-counts.json"


def update_word_counts(to_add: dict[str, int]):
    existing_counts = {}

    if dict_path.exists():
        with open(dict_path, "r", encoding="utf-8") as f:
            existing_counts = load(f)

    existing_counts.update(to_add)

    with open(dict_path, "w", encoding="utf-8") as f:
        dump(existing_counts, f, indent=4, ensure_ascii=False)


def analyze_relative_word_freq(mode: str, n: int, chart_path=None):
    data = get_relative_freq_table(mode=mode, n=n)

    # data = DataFrame({
    #     "word": ["hello", "world", "python"],
    #     "frequency in the article": [0.05, 0.03, 0.01],
    #     "frequency in the wiki language": [0.08, 0.02, 0.015]
    # })

    print(data)

    if chart_path is not None:
        dyn_width = max(10, int(n * 0.8))
        data.plot(
            x="word",
            y=["frequency in the article", "frequency in the wiki language"],
            kind="bar",
            color=["royalblue", "indianred"],
            title=(f"Top {n} words by relative frequency "
                   f"(sorted by appearance in {mode})"),
            xlabel="",
            ylabel="Frequency",
            legend=True,
            figsize=(dyn_width, 6),
            rot=0
        )
        plt.savefig(chart_path)


def get_relative_freq_table(mode: str, n: int) -> DataFrame:
    word_counts = {}

    if dict_path.exists():
        with open(dict_path, "r", encoding="utf-8") as f:
            word_counts = load(f)

    if mode == "article":
        df = DataFrame(
            list(word_counts.items()),
            columns=["word", "frequency in the article"]
        )

        # Normalizing frequencies to match `word_frequency` scale
        normaliser = 1.1 * df["frequency in the article"].max()
        df["frequency in the article"] = (
            df["frequency in the article"] / normaliser
        )

        df_sorted = df.sort_values(
            by="frequency in the article",
            ascending=False
        ).head(n)

        df_sorted["frequency in the wiki language"] = df_sorted["word"].apply(
            lambda w: word_frequency(w, "en")
        )

        return df_sorted
    elif mode == "language":
        top_words = top_n_list("en", n)

        df = DataFrame({"word": top_words})
        df["frequency in the wiki language"] = df["word"].apply(
            lambda w: word_frequency(w, "en")
        )

        df["frequency in the article"] = df["word"].apply(
            lambda w: word_counts.get(w, 0)
        )

        # Normalizing frequencies to match `word_frequency` scale
        normaliser = 1.1 * df["frequency in the article"].max()
        df["frequency in the article"] = (
            df["frequency in the article"] / normaliser
        )

        return df


def auto_count_words(start_phrase: str, depth: int, wait: float):
    raise NotImplementedError()
