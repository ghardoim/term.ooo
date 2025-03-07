from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from write.writeword import WriteWord

class English(WriteWord):
    def __init__(self, child:list=[]) -> None:

        if not child:
            super().__init__("https://www.nytimes.com/games/wordle/index.html", [(By.XPATH, "//button[@{}]".format(btn))
                for btn in ["class='purr-blocker-card__button'", "data-testid='Accept all-btn'", "data-testid='Play'", "aria-label='Close'"]])

            self.rows = self.find_elements((By.XPATH, "//div[contains(@aria-label, 'Row ')]"))
            self.status = ["correct", "absent", "present"]
            self.language = self.__class__.__name__
            self.not_exist = "tbd"

        else: super().__init__(*child)
        self.actions = ActionChains(self)

    def run(self) -> None:
        super()._run()

    def _write(self, row:WebElement, key:str) -> None:
        self.actions.send_keys_to_element(row, key).perform()

    def _get_guess_position(self, row:WebElement, status:str) -> str:
        return "".join([f" {s.text}{s.get_attribute('aria-label')[0]}"
            for s in row.find_elements(By.XPATH, "//div[@data-state='{}']".format(status))])

    def _get_all(self, row:WebElement, status:str) -> list:
        return row.find_elements(By.XPATH, ".//div[@data-state='{}']".format(status))

class Phrase(English):
    def __init__(self, word_length:int=5) -> None:

        self.word_length = word_length
        super().__init__([f"https://solitaired.com/wordhurdle-{self.word_length}-letter", [(By.ID, "container")]])

        self.rows = self.find_elements(By.CLASS_NAME, "wordhunt-row")
        self.status = ["blockGreen", "blockGrey", "blockGold"]

    def __run(self) -> None:
        self.is_all(self.rows[0], "letter-added", self.word_length)
        (tbd := self.rows[0].find_elements(By.XPATH, ".//div[not(contains(@class, ' block'))]"))

    def _get_guess_position(self, word:WebElement, status:str) -> str:
        return "".join([f" {key.text}{position + 1}"
            for position, key in enumerate(word.find_elements(By.CLASS_NAME, status))])

    def _get_all(self, row:WebElement, status:str) -> list:
        return row.find_elements(By.XPATH, ".//div[contains(@class, '{}')]".format(status))

if "__main__" == __name__:
    English().run()