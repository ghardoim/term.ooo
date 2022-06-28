from utils import remove_accentuation
import requests as rq
import argparse

class FindWord:
    def __init__(self) -> None:
        self.__run()

    def words(letter:str="") -> list:
        _words = map(remove_accentuation, rq.get("https://raw.githubusercontent.com/fserb/pt-br/master/dicio").text.split("\n"))
        _words = list(filter(lambda word: 5 == len(word) and letter in word, _words))
        return [w for w in _words if not any([l for l in range(4) if w[l] == w[l + 1] and "rr" not in w and "ss" not in w])]

    def __run(self) -> None:
        parser = argparse.ArgumentParser(prog="find words with five letters", usage="%(prog)s")
        parser.add_argument("--with_", type=str, required=True)
        parser.add_argument("--not-has", type=str, required=True)
        parser.add_argument("--has", type=str)
        parser.add_argument("--not-is-in", type=str, nargs="+")
        parser.add_argument("--is-in", type=str, nargs="+")
        self.params = parser.parse_args()

        for _word in FindWord.words(self.params.with_):
            can_print = True if self.__not_contains(_word) else False
            if can_print and self.params.has: can_print = True if self.__contains(_word) else False
            if can_print and self.params.is_in: can_print = True if self.__is_in(_word) else False
            if can_print and self.params.not_is_in: can_print = True if self.__not_is_in(_word) else False
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
        for letter, position in self.params.is_in:
            if letter != word[int(position) - 1]: return False
        return True

    def __not_is_in(self, word:str) -> bool:
        for letter, position in self.params.not_is_in:
            if letter == word[int(position) - 1]: return False
        return True

if "__main__" == __name__: FindWord()