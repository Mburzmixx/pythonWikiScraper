# Main module.
from wiki_scraper.cli import parse_args
from wiki_scraper.controller import Controller
from wiki_scraper.exceptions import ArticleNotFound
from wiki_scraper.utils import OK


def main():
    args = parse_args()
    controller = Controller(args)
    try:
        if controller.run() == OK:
            print("Program exited successfully.")
    except ArticleNotFound as e:
        print("ERROR: Article not found.")


if __name__ == "__main__":
    main()
