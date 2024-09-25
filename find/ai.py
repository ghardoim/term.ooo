import google.generativeai as genai

class AIFinder:
    def __init__(self):
        genai.configure(api_key="")
        self.model = genai.GenerativeModel("gemini-pro")

    def hit(self, filters:dict={}, language:str="", word_length:str="five") -> str:
        """
        This function is used to interact with the AI model to find the word of the day with five letters.
        The filters parameter is used to pass the tips to the AI model to filter the words.
        The filters parameter must be a dictionary with the following keys:
        - HAS | NOT-HAS: string with letters that the word must have or not.
        - IS-IN | NOT-IS-IN: sequences separated by space like A1, where A is a letter and 1 is the position.

        """

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