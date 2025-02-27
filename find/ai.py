from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
import google.generativeai as genai
from find.api import APIFinder
from typing import Iterator
import requests as rq
from os import getenv

API_KEY = getenv("GOOGLE_API_KEY")
CONTEXT = """
    You are playing a game to guess the word of the day.

    Use this list of words as consult base to your guess:
        {WORDS}
    *YOUR GUESS MUST BE ONE OF THE PREVIOUS WORDS*
"""

FIRST_GUESS = CONTEXT + """
    The word must mach with the following instructions:
        - the letters must not repeat.

    Your answer must be in {LANGUAGE}
    {FORMAT}
"""

GUESS = CONTEXT + """
    You are playing a game to guess the word of the day.
    The word must mach with the following instructions:

        - must have the following letters: {HAS}
        - must not contains the following letters: {NOT_HAS}

    Use these sequences. e.g: G1 letter G in the first position, to evaluate if the word must have or must not have the letters located in that position.
        - must be: '{IS_IN}'
        - must not be: '{NOT_IS_IN}'

    Your answer must be in {LANGUAGE}
    {FORMAT}
"""

class AIFinder:
    def __init__(self):
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=API_KEY, temperature=0)
        
        self.parser = PydanticOutputParser(pydantic_object=Guess)
        self.fmt = {"partial_variables":{"FORMAT":self.parser.get_format_instructions()}}

    def hit(self, filters:dict={}, language:str="", word_length:str="five") -> str:
        return self.model.start_chat(history=[{"role": "user", "parts": f"""

            You are like a dictionary, you know every word of the {language} vocabulary.
            Your mission is help to find the word of the day with {word_length} letters.
            For your first guess, is alwyas better to suggest a word which does not repeat any letter.
            After that, you will receive some of the following tips which you need to use to filter your next guesses.

            - HAS: The word must have all of these letters.
            - NOT-HAS: The word must not have all of these letters.

            - IS-IN: Is a sequence like A1, where A is a letter and 1 is the position. The word must have that letter in that position.
            - NOT-IS-IN: Is a sequence like A1, where A is a letter and 1 is the position. The word must not have that letter in that position.

            # They'll be passed as key:value pairs separeted by commas and all of them must be true for the word to be correct.
            # Be sure that your suggestions are in lowercase and have exactly {word_length} letters.

            # If you find more than one word, choose only one at random.
            # Do not suggest the same word twice.

            I'll use the expression 'hit!' following or not by these parameters to ask for the next guess.
            Let's start!

        """}]).send_message("hit! " + ", ".join([f"{key}: '{value}'" for key, value in filters.items() if value])).text

    def guess(self, filters:dict={}, prompt:str="") -> str:
        guess = PromptTemplate(template=prompt, input_variables=["WORDS", "LANGUAGE"] + list(filters.keys()), **self.fmt)

        return (guess | self.llm | self.parser).invoke({**filters,
            "WORDS": [w.page_content for w in HTTPRequestLoader("en-us", filters["LENGTH"]).load()]}).word

class HTTPRequestLoader(BaseLoader):
    def __init__(self, language:str="pt-br", length:int=5) -> None:
        self.words = APIFinder(LANGUAGE=language, WORD_LENGTH=length).words()

    def lazy_load(self) -> Iterator[Document]:
        for word in self.words: yield Document(page_content=word)

class Guess(BaseModel):
    word:str = Field(description="Word which will be used as guess.")