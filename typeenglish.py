from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typeword import TypeWord
from random import randint
from time import sleep

class English(TypeWord):
    def __init__(self) -> None:
        super().__init__("https://www.nytimes.com/games/wordle/index.html")

        self._browser.find_element(By.XPATH, "//button[contains(text(),'ACCEPT')]").click()
        self._browser.find_element(By.CSS_SELECTOR, "[aria-label='Close']").click()
        self._actions = ActionChains(self._browser)

        self._flags, new_words = {"--has": "", "--not-has": "", "--is-in": "", "--not-is-in": ""}, []
        board = self._browser.find_element(By.XPATH, "//div[contains(@class,'Board')]")

        for r, row in enumerate(board.find_elements(By.XPATH, "//div[contains(@class,'Row')]")):
            if self._is_all(row, "empty"):
                while True:

                    self._guess(r, row, new_words, "en-us")
                    if self._is_all(row, "tbd"):
                        [ self._actions.send_keys_to_element(cell, Keys.BACKSPACE).perform() for cell in self._get_all(row, "tbd") ]
                    else: break

            sleep(3)
            self._analyze_guess(row, "correct", "absent", "present")
            if not self._is_all(row, "correct"): new_words = self._get_new_words("en-us")
            else: break

    def _get_all(self, row:WebElement, kind:str) -> list: return row.find_elements(By.CSS_SELECTOR, "[data-state='%s']" % (kind))
    def _get_guesses(self, row:WebElement, kind:str) -> str: return "".join([l.text for l in self._get_all(row, kind)])

    def _get_guess_position(self, row:WebElement, kind:str) -> str:
        return "".join([f" {s.text}{_ + 1}" for _, s in enumerate(row.find_elements(By.CSS_SELECTOR,
            "[aria-roledescription='tile']")) if s.get_attribute("data-state") == kind])

    def _try_this(self, row:WebElement, words:list) -> None:
        self._actions.send_keys_to_element(row, words[randint(0, len(words) - 1)]).perform()
        self._actions.send_keys_to_element(row, Keys.ENTER).perform()

if "__main__" == __name__: English()