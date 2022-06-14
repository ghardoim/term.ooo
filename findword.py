from unicodedata import normalize
from bs4 import BeautifulSoup
import requests as rq
import argparse

class FindWord:
    def __init__(self) -> None:
        self.__run()

    def __run(self) -> None:
        parser = argparse.ArgumentParser(prog="find words with five letters", usage="%(prog)s")

        parser.add_argument("--where", type=str, required=True)
        parser.add_argument("--letter", type=str, required=True)
        parser.add_argument("--not-contains", type=str, required=True)
        parser.add_argument("--contains", type=str)
        parser.add_argument("--is-in", type=str)
        parser.add_argument("--not-in", type=str)

        self.params = parser.parse_args()
        if not self.params.where in ["com", "comecam", "terminadas"]:
            print("\nsay where the letters will be searched")
            return

        self.ou = "-1" if self.params.letter in ["o", "u"] and "com" == self.params.where else ""
        url_search = f"https://www.dicio.com.br/palavras-{self.params.where}-{self.params.letter}-com-5-letras{self.ou}/"

        _words = BeautifulSoup(rq.get(url_search).text, "html.parser")
        _words = _words.find(attrs= {"class": "card"}).find_all("p")[1].text.strip()

        self.__words = normalize("NFD", _words).encode("ascii", "ignore").decode("utf-8")

        for _ in range(0, len(self.__words), 5):
            _word = self.__words[_: _ + 5]
            can_print = True if self.__not_contains(_word) else False

            if can_print and self.params.contains:
                can_print = True if self.__contains(_word) else False

            if can_print and self.params.is_in:
                can_print = True if self.__is_in(_word) else False

            if can_print and self.params.not_in:
                can_print = True if self.__not_in(_word) else False

            if can_print:
                print(_word)

    def __contains(self, word:str) -> bool:
        for l in self.params.contains:
            if l not in word:
                return False
        return True

    def __not_contains(self, word:str) -> bool:
        for l in self.params.not_contains:
            if l in word:
                return False
        return True

    def __is_in(self, word:str) -> bool:
        letter, position = self.params.is_in
        return letter == word[int(position) - 1]

    def __not_in(self, word:str) -> bool:
        letter, position = self.params.not_in
        return letter != word[int(position) - 1]

FindWord()