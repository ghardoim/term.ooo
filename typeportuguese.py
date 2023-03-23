from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from findword import FindWord as fw
from typeword import TypeWord
from random import randint
from time import sleep
from sys import argv

class Portuguese(TypeWord):
    def __init__(self, nwords:str="") -> None:
        super().__init__(f"https://term.ooo/{nwords}")
        self._browser.find_element(By.TAG_NAME, "wc-modal").click()

        for b in range(int(nwords) if nwords else 1):
            flags = {"--has": "", "--not-has": "", "--is-in": "", "--not-is-in": ""}
            for r, row in enumerate(self._browser.find_element(By.ID, f"board{b}").shadow_root.find_elements(By.CSS_SELECTOR, "[termo-row]")):
                if self._is_all(row, "empty"):
                    while True:
                        self._guess(r, row, flags, "pt-br")
                        if self._browser.find_element(By.TAG_NAME, "wc-notify").shadow_root.find_element(By.ID, "msg").is_displayed():
                            [ cell.send_keys(Keys.BACKSPACE) for cell in self._get_all(row, "letter") ]
                        else: break

                while 0 != len(self._get_all(row, "empty")): sleep(1)
                flags = self._analyze_guess(row, flags, "right", "wrong", "place")
                if self._is_all(row, "right") or self._browser.find_element(By.TAG_NAME, "wc-notify").is_enabled(): break
            if self._browser.find_element(By.TAG_NAME, "wc-modal").is_displayed(): break

    def _get_all(self, row:WebElement, kind:str) -> list: return row.shadow_root.find_elements(By.CLASS_NAME, kind)
    def _get_guesses(self, row:WebElement, kind:str) -> str: return fw.remove_accent(super()._get_guesses(row, kind))

    def _get_guess_position(self, row:WebElement, kind:str) -> str:
        return fw.remove_accent("".join([f" {s.text}{int(s.get_attribute('termo-pos')) + 1}" for _, s in enumerate(self._get_all(row, kind))]))

    def _try_this(self, row:WebElement, words:list) -> None:
        row.send_keys(words[randint(0, len(words) - 1)])
        row.send_keys(Keys.ENTER)

if "__main__" == __name__: Portuguese("".join(argv[1:]))
