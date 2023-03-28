from argparse import ArgumentParser
from unicodedata import normalize
import requests as rq

class FindWord:
    def __init__(self) -> None: self.__run()
    def remove_accent(text: str) -> str: return normalize("NFD", text.lower().strip()).encode("ascii", "ignore").decode("utf-8")

    def words(nletters:int=5, language:str="pt-br") -> list:
        _lang = { "pt-br": "fserb/pt-br/master/dicio", "en-us": "dwyl/english-words/master/words_alpha.txt" }

        _words = map(FindWord.remove_accent, rq.get(f"https://raw.githubusercontent.com/{_lang[language]}").text.split("\n"))
        return list(filter(lambda word: nletters == len(word), _words))

    def __run(self) -> None:
        parser = ArgumentParser(prog="find words filtered out by some criterias", usage="%(prog)s")
        parser.add_argument("--not-has", type=str, default="")
        parser.add_argument("--has", type=str)

        start = parser.add_mutually_exclusive_group()
        start.add_argument("--not-starts-with", type=str)
        start.add_argument("--starts-with", type=str)

        end = parser.add_mutually_exclusive_group()
        end.add_argument("--not-ends-with", type=str)
        end.add_argument("--ends-with", type=str)

        parser.add_argument("--not-contains", type=str)
        parser.add_argument("--contains", type=str)

        parser.add_argument("--not-is-in", type=str, nargs="+")
        parser.add_argument("--is-in", type=str, nargs="+")

        parser.add_argument("--letters-amount", type=int, default=5)
        parser.add_argument("--language", type=str, default="pt-br")
        self.params = parser.parse_args()

        for _word in FindWord.words(self.params.letters_amount, self.params.language):
            can_print = self.__not_has(_word)

            if can_print and self.params.not_starts_with: can_print = not self.__starts_with(_word)
            if can_print and self.params.starts_with: can_print = self.__starts_with(_word)

            if can_print and self.params.not_ends_with: can_print = not self.__ends_with(_word)
            if can_print and self.params.ends_with: can_print = self.__ends_with(_word)

            if can_print and self.params.not_contains: can_print = self.__not_contains(_word)
            if can_print and self.params.contains: can_print = self.__contains(_word)

            if can_print and self.params.not_is_in: can_print = self.__not_is_in(_word)
            if can_print and self.params.is_in: can_print = self.__is_in(_word)

            if can_print and self.params.has: can_print = self.__has(_word)
            if can_print: print(_word)

    def __contains(self, word:str) -> bool: return self.params.contains in word
    def __has(self, word:str) -> bool: return all([l in word for l in self.params.has])
    def __not_contains(self, word:str) -> bool: return self.params.not_contains not in word
    def __not_has(self, word:str) -> bool: return all([l not in word for l in self.params.not_has])
    def __is_in(self, word:str) -> bool: return all([letter == word[int(position) - 1] for letter, position in self.params.is_in])
    def __not_is_in(self, word:str) -> bool: return all([letter != word[int(position) - 1] for letter, position in self.params.not_is_in])
    def __ends_with(self, word:str) -> bool: return word.endswith(self.params.ends_with if self.params.ends_with else self.params.not_ends_with)
    def __starts_with(self, word:str) -> bool: return word.startswith(self.params.starts_with if self.params.starts_with else self.params.not_starts_with)

if "__main__" == __name__: FindWord()
