from abc import ABC, abstractmethod
from Common.Constants import labels_mapping

class ITrainingDataGenerator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.text = ""
        self.intent = -1
        self.slots = {}
        self.generate()

    def __call__(self):
        if (self.text==""):
            raise ValueError("No text has been set for this generator")

        if (self.intent==-1):
            raise ValueError("No intent has been set for this generator")

        return {"text": self.text, "intent": labels_mapping[self.intent], "slots": self.slots}

    @abstractmethod
    def generate(self):
        pass
