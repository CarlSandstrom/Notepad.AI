from ITrainingDataGenerator import ITrainingDataGenerator
from Common.Constants import SAVE_FILE
import random
import os


class SaveFile(ITrainingDataGenerator):
    _data_is_loaded = False

    @classmethod
    def load_data(cls):
        if not cls._data_is_loaded:
            current_path = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_path, "data/")
            cls.prefixes = open(os.path.join(data_path, "filename_prefix.list"), "r").read().splitlines()
            cls.suffixes = open(os.path.join(data_path, "filename_suffix.list"), "r").read().splitlines()
            cls._data_is_loaded = True

    def generate(self):
        self.load_data()
        filename = self._random_filename()
        structures = [
            (f'Save file as "{filename}"', filename),
            (f'Save as "{filename}"', filename),
            (f'Save this document as "{filename}"', filename),
            (f'Could you save this as "{filename}"?', filename),
            (f'I need to save this file. Name it "{filename}"', filename),
            (f"Save the current document", ""),
            (f"Save my work", ""),
            (f'Save changes to "{filename}"', filename),
            (f'Create a new file named "{filename}" and save it', filename),
            (f'Save a copy as "{filename}"', filename),
        ]
        text, filename = random.choice(structures)
        slots = {"FILENAME": filename} if filename else {}
        self.text = text
        self.slots = slots
        self.intent = SAVE_FILE

    def _random_filename(self):

        return f"{random.choice(self.prefixes)}_{random.randint(1, 100)}.{random.choice(self.suffixes)}"
