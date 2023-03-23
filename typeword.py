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

    def _guess(self, nguess:int, row:WebElement, flags:dict, lang:str, len_word:int=5) -> None:
        if 0 == nguess: self._try_this(row, FindWord.words(language=lang, nletters=len_word))
        else: self._try_this(row, self._get_new_words(lang, flags, len_word))
        sleep(1)

    def _analyze_guess(self, row:WebElement, flags:dict, yes:str, no:str, maybe:str) -> dict:

        flags["--not-is-in"] += f" {self._get_guess_position(row, maybe)} {self._get_guess_position(row, no)}"
        flags["--has"] += f"{self._get_guesses(row, yes)}{self._get_guesses(row, maybe)}"
        flags["--not-has"] = "".join(set(flags["--not-has"]).difference(flags["--has"]))
        flags["--not-is-in"] = self._clear_isin(flags["--not-is-in"])
        flags["--is-in"] += " " + self._get_guess_position(row, yes)
        flags["--is-in"] = self._clear_isin(flags["--is-in"])
        flags["--not-has"] += self._get_guesses(row, no)
        flags["--has"] = "".join(set(flags["--has"]))
        return flags

    def _get_new_words(self, lang:str, flags:dict, amout_letters:int=5) -> list:
        cmd_find = f"python findword.py --language {lang} --letters-amount {amout_letters} "
        cmd_find += " ".join([f"{key} {value}" for key, value in flags.items() if value]).lower()
        return run(cmd_find.split(" "), stdout=PIPE, text=True, shell=True).stdout.strip().split("\n")

    def __del__(self) -> None: self._browser.close()
    def _is_all(self, row:WebElement, kind:str) -> bool: return 5 == len(self._get_all(row, kind))
    def _clear_isin(self, flag:str) -> str: return " ".join(sorted(filter(lambda l: l, set(flag.split(" ")))))
    def _get_guesses(self, row:WebElement, kind:str) -> str: return "".join([l.text for l in self._get_all(row, kind)])
