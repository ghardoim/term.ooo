from selenium.webdriver.common.by import By
from selenium.webdriver import Safari
from time import sleep

class Puzzle(Safari):
    def __init__(self, url:str):
        super().__init__()

        self.get("https://www.nytimes.com/" + url)
        self.maximize_window()
        sleep(2)

        for button in ["//button[contains(text(), '{}')]".format(btn) for btn in ["Reject all", "Continue", "Play"]]:
            self.execute_script("arguments[0].click()", self.find_element(By.XPATH, button))

    def end(self) -> None:
        self.close()
        self.quit()