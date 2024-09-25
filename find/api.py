from argparse import ArgumentParser, Namespace
import requests as rq

class APIFinder:
    def __init__(self, HAS:str=None, NOT_HAS:str=None, IS_IN:str=None, NOT_IS_IN:str=None, WORD_LENGTH:int=5, LANGUAGE:str="pt-br") -> None:

        self.kwargs = Namespace(**{
            "WORD_LENGTH": WORD_LENGTH, "LANGUAGE": LANGUAGE,
            "HAS": HAS, "NOT_HAS": NOT_HAS, "IS_IN": IS_IN, "NOT_IS_IN": NOT_IS_IN
        })

    def words(self) -> list:
        language, splitby = {
            "pt-br": ("fserb/pt-br/master/dicio", "\n"),
            "en-us": ("dwyl/english-words/master/words_alpha.txt", "\r\n")
        }[self.kwargs.LANGUAGE]

        return list(filter(lambda word: self.kwargs.WORD_LENGTH == len(word),
            rq.get(f"https://raw.githubusercontent.com/{language}").text.split(splitby)))

    def filter(self) -> list:
        verifications = [ (self.__has, self.kwargs.HAS), (self.__not_has, self.kwargs.NOT_HAS),
            (self.__is_in, self.kwargs.IS_IN), (self.__not_is_in, self.kwargs.NOT_IS_IN) ]

        return list(filter(lambda word: all([ verify(word) for verify, args in verifications if args]), self.words()))

    def cmd_run(self) -> None:
        parser = ArgumentParser()

        parser.add_argument("--NOT-HAS", type=str, default="")
        parser.add_argument("--HAS", type=str, default="a")

        parser.add_argument("--NOT-IS-IN", type=str, nargs="+")
        parser.add_argument("--IS-IN", type=str, nargs="+")

        parser.add_argument("--LANGUAGE", type=str, default="pt-br")
        parser.add_argument("--WORD-LENGTH", type=int, default=5)

        self.kwargs = parser.parse_args()
        print(self.filter())

    def __has(self, word:str) -> bool:
        return all([key.lower() in word for key in self.kwargs.HAS])

    def __not_has(self, word:str) -> bool:
        return all([key.lower() not in word for key in self.kwargs.NOT_HAS])

    def __is_in(self, word:str) -> bool:
        return all([key.lower() == word[int(value) - 1]
            for key, value in self._split(self.kwargs.IS_IN)])

    def __not_is_in(self, word:str) -> bool:
        return all([key.lower() != word[int(value) - 1]
            for key, value in self._split(self.kwargs.NOT_IS_IN)])

    def _split(self, parameters:str|list) -> list:
        return parameters if isinstance(parameters, list) else parameters.split(" ")

if "__main__" == __name__:
    APIFinder().cmd_run()