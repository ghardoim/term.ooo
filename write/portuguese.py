from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from write.writeword import WriteWord

class Portuguese(WriteWord):
    def __init__(self, how_many:str="") -> None:

        self.status = ["right", "wrong", "place"]
        self.language = self.__class__.__name__
        self.not_exist = "empty"

        super().__init__(f"https://term.ooo/{how_many}", [(By.TAG_NAME, "wc-modal")])

    def run(self, boards:int=1) -> None:
        for board in range(boards):

            self.rows = self.find_element(By.ID, f"board{board}").shadow_root.find_elements(By.CSS_SELECTOR, "[termo-row]")
            super()._run()

    def _write(self, row:WebElement, key:str) -> None:
        row.send_keys(key)

    def _get_guess_position(self, row:WebElement, status:str) -> str:
        return "".join([f" {s.text}{int(s.get_attribute('termo-pos')) + 1}" for s in self._get_all(row, status)])

    def _get_all(self, row:WebElement, status:str) -> list:
        return row.shadow_root.find_elements(By.CLASS_NAME, status)

if "__main__" == __name__:
    Portuguese().run()