from playwright.sync_api._generated import Locator
from playwright.sync_api import sync_playwright
from utils import remove_accentuation
from subprocess import run, PIPE
from random import randint
from sys import argv

class TypeWord:
    def __init__(self) -> None:
        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch(headless=False)
        self.__initials_words = ["extra", "vespa", "muito", "coisa", "tribo", "bunda", "jeito"] 
        self.__url = "https://term.ooo/"

    def __del__(self) -> None:
        self.__browser.close()
        self.__play.stop()

    def run(self, nterm: str = "") -> None:
        self.page = self.__browser.new_page()
        self.page.goto(f"{self.__url}/{nterm}")
        self.page.click("#help")

        self.__try_with_initial_words(self.page.locator(f"#board0"), 0)
        self.__find_word(int(nterm) if nterm else 0)

    def __find_word(self, nterm: int, nboard: int = 0):
        tries = self.page.locator(f"#board{nboard}")

        self.flags = { "--has": "", "--not-has": "", "--is-in": "", "--not-is-in": "" }
        for _try in range(1, int(tries.get_attribute("rows"))):
            last = tries.locator("[aria-label='palavra %i']" % (_try - 1))

            self.flags["--has"] += self.__get_contained_words(last)
            self.flags["--has"] = ''.join(set(self.flags["--has"]))

            self.flags["--not-has"] += self.__check_hit_in_this_try(last, 'wrong')
            self.flags["--is-in"] += f" {self.__check_hit_in_this_try(last, 'right')}"
            self.flags["--not-is-in"] += f" {self.__check_hit_in_this_try(last, 'place')}"

            if 5 == last.locator(f".letter.right").count():
                nboard += 1
                if (nboard < nterm):
                    self.__find_word(nterm, nboard)

            elif 5 == last.locator(f".letter.wrong").count():
                self.__try_with_initial_words(tries, _try)

            elif tries.locator("[aria-label='palavra %i']" % _try).locator(".letter.empty").count():
                    term_cmd = f"find --with {self.flags['--has'][0]}"
                    term_cmd += f" --has {self.flags['--has'][1:]}" if self.flags['--has'][1:] else ""
                    term_cmd += f" --not-has {''.join(set(''.join([n for n in self.flags['--not-has'] if n not in self.flags['--has']]))).strip()}"
                    for key, value in self.flags.items():
                        if "--is-in" == key: term_cmd += f" --is-in {' '.join(set(value.split(' '))).strip()}" if value.strip() else ""
                        if "--not-is-in" == key: term_cmd += f" --not-is-in {' '.join(set(value.split(' '))).strip()}" if value.strip() else ""

                    words = run(term_cmd.split(" "), stdout=PIPE, text=True).stdout.split("\n")
                    print(f"#board{nboard}", "[aria-label='palavra %i']" % _try, term_cmd, words[0])
                    self.__try(tries, _try, words[0])

    def __try(self, tries: Locator, ntry: int, word: str) -> None:
        attempt = tries.locator("[aria-label='palavra %i']" % ntry)
        attempt.type(word)
        attempt.press("Enter")
        self.page.wait_for_timeout(2000)

    def __try_with_initial_words(self, tries: Locator, ntry: int) -> None:
        _ = randint(0, len(self.__initials_words) - 1)
        self.__try(tries, ntry, self.__initials_words[_])
        del self.__initials_words[_]

    def __check_hit_in_this_try(self, last_try: Locator, kick_kind: str) -> str:
        matched, what_to_search = last_try.locator(f".letter.{kick_kind}"), ""
        for l in range(matched.count()):
            letter = remove_accentuation(matched.nth(l).text_content())
            position = int(matched.nth(l).get_attribute('termo-pos')) + 1

            what_to_search += f" {letter}{position}" if "wrong" not in kick_kind else letter
        return what_to_search.strip()

    def __get_contained_words(self, last_try: Locator) -> str:
        _has = [last_try.locator(f".letter.{_}") for _ in ["right", "place"]]
        return "".join(["".join([remove_accentuation(_.nth(l).text_content()) for l in range(_.count())]) for _ in _has]) 

TypeWord().run("".join(argv[1:]))