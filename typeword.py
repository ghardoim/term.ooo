from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from subprocess import run, PIPE
from selenium import webdriver
from findword import FindWord
from time import sleep

class TypeWord:
    def __init__(self, url:str) -> None:
        self._browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self._browser.maximize_window()
        self._browser.get(url)

    def _guess(self, nguess:int, row:WebElement, newwords:list, lang:str) -> None:
        if 0 == nguess: self._try_this(row, FindWord.words(language=lang))
        else: self._try_this(row, newwords)
        sleep(1)

    def _analyze_guess(self, row:WebElement, yes:str, no:str, maybe:str) -> None:
        self._flags["--has"] += f"{self._get_guesses(row, yes)}{self._get_guesses(row, maybe)}"
        self._flags["--has"] = "".join(set(self._flags["--has"]))

        self._flags["--not-has"] += self._get_guesses(row, no)
        self._flags["--not-has"] = "".join(set(self._flags["--not-has"]).difference(self._flags["--has"]))

        self._flags["--is-in"] += " " + self._get_guess_position(row, yes)
        self._flags["--is-in"] = self._clear_isin(self._flags["--is-in"])

        self._flags["--not-is-in"] += f" {self._get_guess_position(row, maybe)} {self._get_guess_position(row, no)}"
        self._flags["--not-is-in"] = self._clear_isin(self._flags["--not-is-in"])

    def _get_new_words(self, lang:str) -> list:
        cmd_find = f"python findword.py --language {lang} "
        cmd_find += " ".join([f"{key} {value}" for key, value in self._flags.items() if value]).lower()
        return run(cmd_find.split(" "), stdout=PIPE, text=True, shell=True).stdout.strip().split("\n")

    def __del__(self) -> None: self._browser.close()
    def _is_all(self, row:WebElement, kind:str) -> bool: return 5 == len(self._get_all(row, kind))
    def _clear_isin(self, flag:str) -> str: return " ".join(sorted(filter(lambda l: l, set(flag.split(" ")))))
