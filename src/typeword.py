from playwright.sync_api._generated import Locator
from playwright.sync_api import sync_playwright
from utils import remove_accentuation
from datetime import datetime as dt
from subprocess import run, PIPE
from random import randint
from sys import argv

class TypeWord:
    def __init__(self) -> None:
        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch(headless=False)
        self.__initials_words = ["extra", "vespa", "muito", "coisa", "negro", "bicho", "bunda", "jeito", "fizer", "quilo"]
        self.__already_tried = []
        self.__url = "https://term.ooo/"

    def __del__(self) -> None:
        self.page.screenshot(path=f"img/{self.nterm if self.nterm else 1}w {dt.now().strftime('%d-%m')}.png")
        self.__browser.close()
        self.__play.stop()

    def run(self, nterm: int = 0) -> None:
        self.page = self.__browser.new_page()
        self.nterm = nterm
        self.nboard = 0

        self.page.goto(f"{self.__url}/{self.nterm if self.nterm else ''}")
        self.page.click("#help")

        self.__find_word()

    def __find_word(self) -> None:
        self.board = self.page.locator(f"#board{self.nboard}")

        self.flags, row = { "--with": "", "--has": "", "--not-has": "", "--is-in": "", "--not-is-in": "" }, 0
        while row < int(self.board.get_attribute("rows")):
            if 0 == row and 0 == self.nboard: self.__try_with_initials_words(row)
            last = self.board.locator("[aria-label='palavra %i']" % (row - 1))

            self.flags["--has"] += self.__get_letters(last, "right")
            self.flags["--has"] += self.__get_letters(last, "place")
            self.flags["--has"] = ''.join(set(self.flags["--has"])).strip()

            self.flags["--not-has"] += self.__get_letters(last, 'wrong')
            self.flags["--not-has"] = ''.join(set([_ for _ in self.flags['--not-has'] if _ not in self.flags['--has']])).strip()

            self.flags["--is-in"] += f" {self.__get_letter_position(last, 'right')}"
            self.flags["--is-in"] = ' '.join(set(self.flags["--is-in"].strip().split(' '))).strip()

            self.flags["--not-is-in"] += f" {self.__get_letter_position(last, 'place')}"
            self.flags["--not-is-in"] += f" {self.__get_letter_position(last, 'wrong')}"
            self.flags["--not-is-in"] = ' '.join(set(self.flags["--not-is-in"].strip().split(' '))).strip()

            if self.__is_all(last, "wrong"):
                self.__try_with_initials_words(row)

            elif self.__is_all(last, "right"):
                self.nboard += 1
                if (self.nboard < self.nterm): self.__find_word()

            elif self.__is_all(last, "empty"):
                row -= 1
                word = self.words[randint(0, len(self.words) - 1)]
                current = self.board.locator("[aria-label='palavra %i']" % row)

                letters = current.locator(".empty")
                for _ in range(letters.count()):
                    letters.nth(_).click()
                    letters.nth(_).type(word[_])
                current.press("Enter")

                self.words.remove(word)
                self.__already_tried.append(word)

            elif self.__is_all(self.board.locator("[aria-label='palavra %i']" % row), "empty"):
                self.flags["--with"] = self.flags["--has"][0]
                self.flags["--has"] = self.flags["--has"][1:] if self.flags["--has"][1:] else ""

                self.cmd_find = "findterm"
                for key, value in self.flags.items():
                    if value: self.cmd_find += f" {key} {value}"

                self.words = run(self.cmd_find.split(" "), stdout=PIPE, text=True).stdout.strip().split("\n")
                word = self.words[randint(0, len(self.words) - 1)]

                while word in self.__already_tried:
                    self.words.remove(word)
                    word = self.words[randint(0, len(self.words) - 1)]
                if word: self.__try_with_this(row, word)
                else: self.__try_with_initials_words(row)
            row += 1

    def __is_all(self, _try: Locator, _type: str) -> bool:
        return 5 == _try.locator(f".letter.{_type}").count()

    def __try_with_this(self, nrow: int, word: str) -> None:
        _line = self.board.locator("[aria-label='palavra %i']" % nrow)
        _line.type(word)
        _line.press("Enter")

        self.page.wait_for_timeout(2000)
        self.__already_tried.append(word)

    def __try_with_initials_words(self, nrow: int) -> None:
        _ = randint(0, len(self.__initials_words) - 1)

        self.__try_with_this(nrow, self.__initials_words[_])
        del self.__initials_words[_]

    def __get_letter_position(self, _try: Locator, _type: str) -> str:
        lp, squares = "", _try.locator(f".letter.{_type}")

        for _ in range(squares.count()):
            letter = remove_accentuation(squares.nth(_).text_content())
            position = int(squares.nth(_).get_attribute('termo-pos')) + 1

            if _type in ["right", "place"] or ("wrong" == _type and letter in self.flags["--has"]):
                lp += f" {letter}{position}"
        return lp.strip()

    def __get_letters(self, _try: Locator, _type: str) -> str:
        squares = _try.locator(f".letter.{_type}")
        return "".join([remove_accentuation(squares.nth(_).text_content()) for _ in range(squares.count())])

TypeWord().run("".join(argv[1:]))