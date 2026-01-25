from wiki_scraper.scraper import Scraper
from json import dump

phrase_big_article = "Villainous_team"
phrase_low_conf_score = "Fairy_(type)"

path_big_article = "wiki_big_article_wc.json"
path_low_conf_score = "wiki_low_conf_score_wc.json"


def write_dict_to_file(d: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        dump(d, f, ensure_ascii=False, indent=4)


def main():
    scraper1 = Scraper(phrase=phrase_big_article)
    article1 = scraper1.scrape()
    wiki_big_article_wc = article1.count_words()
    write_dict_to_file(
        d=wiki_big_article_wc,
        path=path_big_article
    )

    scraper2 = Scraper(phrase=phrase_low_conf_score)
    article2 = scraper2.scrape()
    low_conf_score_article_wc = article2.count_words()
    write_dict_to_file(
        d=low_conf_score_article_wc,
        path=path_low_conf_score
    )

    print("Successfully wrote word count dictionaries to files!")


if __name__ == "__main__":
    main()
