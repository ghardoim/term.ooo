from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Safari
from unicodedata import normalize
from find.api import APIFinder
from random import choice
from time import sleep

class WriteWord(Safari):
    def __init__(self, url:str, waits_elements:list[tuple], language:str="pt-br", word_length:int=5) -> None:
        super().__init__()

        self.api = APIFinder(lang=language, length=word_length)
        self.waits = WebDriverWait(self, 10)
        self.maximize_window()
        self.get(url)

        for btn in waits_elements: self.waits.until(EC.element_to_be_clickable(btn)).click()

    def _run(self) -> None:
        self.flags = { "HAS": "", "IS-IN": "", "NOT-HAS": "", "NOT-IS-IN": "" }

        for row in self.rows:
            if self.is_all(row, self.not_exist):

                while True:
                    [ self._write(row, key) for key in [choice(self.api.filter()), Keys.ENTER]]
                    sleep(2)

                    if not (tbd := self._get_all(row, self.not_exist)): break
                    [ self._write(letter, Keys.BACKSPACE) for letter in tbd ]

            sleep(2)
            if self.is_all(row, self.status[0]): break
            self.flags = self.analyze_guess(row, self.flags, *self.status)

            for key, value in self.flags.items():
                self.api.kwargs.__dict__[key.replace("-", "_")] = value

    def analyze_guess(self, row:WebElement, flags:dict, yes:str, no:str, maybe:str) -> dict:

        flags["NOT-IS-IN"] += f" {self._get_guess_position(row, maybe)} {self._get_guess_position(row, no)}"
        flags["HAS"] += f"{self.get_guesses(row, yes)}{self.get_guesses(row, maybe)}"
        flags["IS-IN"] += " " + self._get_guess_position(row, yes)
        flags["NOT-HAS"] += self.get_guesses(row, no)

        flags["NOT-HAS"] = "".join(set(flags["NOT-HAS"]).difference(flags["HAS"]))
        flags["NOT-IS-IN"] = self.clear_isin(flags["NOT-IS-IN"])
        flags["IS-IN"] = self.clear_isin(flags["IS-IN"])
        flags["HAS"] = "".join(set(flags["HAS"]))

        return flags
    
    def clear_isin(self, flag:str) -> str: return " ".join(sorted(filter(lambda l: l, set(flag.split(" ")))))
    def is_all(self, row:WebElement, status:str, word_length:int=5) -> bool: return word_length == len(self._get_all(row, status))

    def get_guesses(self, row:WebElement, status:str) -> str:
        return normalize("NFD", "".join([l.text for l in self._get_all(row, status)]).lower().strip()).encode("ascii", "ignore").decode("utf-8")

    def __del__(self) -> None:
        self.close()
        self.quit()