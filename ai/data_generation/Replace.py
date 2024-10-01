from ITrainingDataGenerator import ITrainingDataGenerator
from Common.Constants import REPLACE
import random
import os


class Replace(ITrainingDataGenerator):
    _data_is_loaded = False

    @classmethod
    def load_data(cls):
        if not cls._data_is_loaded:
            current_path = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_path, "data/")
            cls.words = open(os.path.join(data_path, "words.list"), "r").read().splitlines()
            cls._data_is_loaded = True

    def generate(self):
        self.load_data()
        old_word = self._random_word()
        new_word = self._random_word()
        structures = [
            (f'Replace "{old_word}" with "{new_word}"', old_word, new_word),
            (f'Find "{old_word}" and replace it with "{new_word}"', old_word, new_word),
            (f'Change all instances of "{old_word}" to "{new_word}"', old_word, new_word),
            (f'I need to replace "{old_word}" with "{new_word}"', old_word, new_word),
            (f'Can you replace "{old_word}" for me?', old_word, ""),
            (f'Replace "{old_word}"', old_word, ""),
            (f"Find and replace in the document", "", ""),
            (f'Substitute "{old_word}" with "{new_word}" throughout', old_word, new_word),
            (f'Replace every occurrence of "{old_word}" with "{new_word}"', old_word, new_word),
            (f'Search for "{old_word}" and replace with "{new_word}"', old_word, new_word),
        ]
        text, search_term, replace_term = random.choice(structures)
        slots = {}
        slots["SEARCH_TERM"] = search_term if search_term else ""
        slots["REPLACE_TERM"] = replace_term if replace_term else " "
        self.text = text
        self.slots = slots
        self.intent = REPLACE

    def _random_word(self):

        number_of_words = random.uniform(1, 10)
        word_string = ""
        for i in range(int(number_of_words)):
            if len(word_string) > 0:
                word_string = "{} ".format(word_string)
            word_string = "{}{}".format(word_string, random.choice(self.words))

        return word_string
