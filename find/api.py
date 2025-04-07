from argparse import ArgumentParser, Namespace
import requests as rq

class APIFinder:
    def __init__(self, length:int=5, lang:str="pt-br") -> None:
        self.kwargs = Namespace(WORD_LENGTH=length, LANGUAGE=lang, REPEATED=None, SEQUENCE=None,
            HAS=None, NOT_HAS=None, IS_IN=None, NOT_IS_IN=None)

        url, splitby = {
            "pt-br": ("fserb/pt-br/master/dicio", "\n"),
            "en-us": ("dwyl/english-words/refs/heads/master/words_alpha.txt", "\r\n")
        }[lang]
        self.__words = [ word for word in rq.get("https://raw.githubusercontent.com/" + url).text.split(splitby) ]

    def filter(self) -> list:
        verifications = [
            (self.__has, self.kwargs.HAS), (self.__not_has, self.kwargs.NOT_HAS),
            (self.__is_in, self.kwargs.IS_IN), (self.__not_is_in, self.kwargs.NOT_IS_IN),
            (self.__is_repeated, self.kwargs.REPEATED), (self.__has_sequence, self.kwargs.SEQUENCE)
        ]
        _words = [ w for w in self.__words if self.kwargs.WORD_LENGTH == len(w) ]
        return [ w for w in _words if all([ verify(w) for verify, args in verifications if args]) ]

    def cmd_run(self) -> None:

        (parser := ArgumentParser()).add_argument("--LANGUAGE", type=str, default="pt-br")
        parser.add_argument("--WORD-LENGTH", type=int, default=5)
        parser.add_argument("--NOT-HAS", type=str, default="")
        parser.add_argument("--HAS", type=str, default="")

        parser.add_argument("--NOT-IS-IN", type=str, nargs="+")
        parser.add_argument("--IS-IN", type=str, nargs="+")

        parser.add_argument("--REPEATED", type=str, nargs="+")
        parser.add_argument("--SEQUENCE", type=str, default="")

        self.kwargs = parser.parse_args()
        print(self.filter())

    def __has(self, word:str) -> bool:
        return all([key.lower() in word for key in self.kwargs.HAS])

    def __not_has(self, word:str) -> bool:
        return all([key.lower() not in word for key in self.kwargs.NOT_HAS])

    def __is_in(self, word:str) -> bool:
        return all([key.lower() == word[int(value) - 1] for key, value in self._split(self.kwargs.IS_IN)])

    def __not_is_in(self, word:str) -> bool:
        return all([key.lower() != word[int(value) - 1] for key, value in self._split(self.kwargs.NOT_IS_IN)])

    def __is_repeated(self, word:str) -> bool:
        return all([word.count(key) == int(value) for value, key in self._split(self.kwargs.REPEATED)])
    
    def __has_sequence(self, word:str) -> bool:
        return self.kwargs.SEQUENCE in word

    def _split(self, parameters:str|list) -> list:
        return parameters if isinstance(parameters, list) else parameters.split(" ")

if "__main__" == __name__:
    APIFinder().cmd_run()