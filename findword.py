from unicodedata import normalize
from bs4 import BeautifulSoup
import requests as rq
import argparse

class FindWord:
    def __init__(self) -> None: self.__run()

    def __run(self) -> None:
        parser = argparse.ArgumentParser(prog="find words with five letters", usage="%(prog)s")

        parser.add_argument("--start", type=str)
        parser.add_argument("--with_", type=str)
        parser.add_argument("--end", type=str)
        parser.add_argument("--has", type=str)
        parser.add_argument("--not-has", type=str, required=True)
        parser.add_argument("--is_", type=str, nargs="+")
        parser.add_argument("--not-is", type=str, nargs="+", )

        self.params = parser.parse_args()
        if self.params.start is not None: where, letter = "comecam", self.params.start
        if self.params.with_ is not None: where, letter = "contem", self.params.with_
        if self.params.end is not None: where, letter = "terminadas", self.params.end

        match letter:
            case "a": letters = ["a", "á", "â", "ã"]
            case "o": letters = ["o", "ó", "ô", "õ"]
            case "e": letters = ["e", "é", "ê"]
            case "i": letters = ["i", "í"]
            case "u": letters = ["u", "ú"]
            case "c": letters = ["c", "ç"]
            case _: letters = list(letter)

        for l in letters:
            url_search = f"https://www.dicio.com.br/pesquisa-avancada/?tipo={where}&qword={l}&letras=5"

            _words = BeautifulSoup(rq.get(url_search).text, "html.parser")
            for p in _words.find(attrs= {"class": "card"}).find_all("p")[1:]:

                self.__words = normalize("NFD", p.text.strip()).encode("ascii", "ignore").decode("utf-8")
                for _ in range(0, len(self.__words), 5):
                    _word = self.__words[_: _ + 5]
                    can_print = True if self.__not_contains(_word) else False

                    if can_print and self.params.has: can_print = True if self.__contains(_word) else False
                    if can_print and self.params.is_: can_print = True if self.__is_in(_word) else False
                    if can_print and self.params.not_is: can_print = True if self.__not_is_in(_word) else False
                    if can_print: print(_word)

    def __contains(self, word:str) -> bool:
        for l in self.params.has:
            if l not in word: return False
        return True

    def __not_contains(self, word:str) -> bool:
        for l in self.params.not_has:
            if l in word: return False
        return True

    def __is_in(self, word:str) -> bool:
        for letter, position in self.params.is_:
            if letter != word[int(position) - 1]: return False
        return True

    def __not_is_in(self, word:str) -> bool:
        for letter, position in self.params.not_is:
            if letter == word[int(position) - 1]: return False
        return True

FindWord()