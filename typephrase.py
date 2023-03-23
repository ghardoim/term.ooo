from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typeword import TypeWord
from random import randint
from time import sleep

class Phrase(TypeWord):
    def __init__(self) -> None:
        super().__init__("https://solitaired.com/phrazle")

        self._browser.find_element(By.CLASS_NAME, "close").click()
        self._actions = ActionChains(self._browser)

        for r, row in enumerate(self._browser.find_element(By.CLASS_NAME, "game_area").find_elements(By.CLASS_NAME, "wordhunt-row")):
            words = list(filter(lambda w: not w.find_elements(By.CLASS_NAME, "blockSpace"), row.find_elements(By.CLASS_NAME, "wordBreak")))

            if 0 == r: flags = {w: {"--has": "", "--not-has": "", "--is-in": "", "--not-is-in": ""} for w, _ in enumerate(words)}
            for w, word in enumerate(words):

                size = len(word.find_elements(By.CLASS_NAME, "row_block"))
                while True:

                    self._guess(r, row, flags[w], "en-us", size)
                    if w + 1 == len(words):

                        self._actions.send_keys_to_element(row, Keys.ENTER).perform()
                        sleep(sum([len(w.find_elements(By.CLASS_NAME, "row_block")) for w in words]) // 2)

                    if str(w + 1) in self._browser.find_element(By.ID, "notification").text:
                        [self._actions.send_keys_to_element(l, Keys.BACKSPACE).perform() for l in word.find_elements(By.CLASS_NAME, "row_block")]
                    else: break

            for w, word in enumerate(words):
                for color in ["Grey", "Purple"]: flags[w] = self._analyze_guess(word, flags[w], "Green", color, "Gold")
            if self._browser.find_element(By.CLASS_NAME, "close").is_displayed(): break

    def _get_guess_position(self, word:WebElement, kind:str) -> str:
        return "".join([f" {s.text}{_ + 1}" for _, s in enumerate(word.find_elements(By.CLASS_NAME, "row_block")) if kind in s.get_attribute("class")])

    def _get_all(self, row:WebElement, kind:str) -> list: return row.find_elements(By.CLASS_NAME, f"block{kind}")
    def _try_this(self, row:WebElement, words:list) -> None: self._actions.send_keys_to_element(row, words[randint(0, len(words) - 1)]).perform()

if "__main__" == __name__: Phrase()