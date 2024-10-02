from PyQt5.QtCore import QObject, pyqtSignal
from ai.text_processing.TextProcessing import CommandDecoder


class AIService(QObject):
    def __init__(self):
        super().__init__()

        self._command_decoder = CommandDecoder()

    def process_text(self, text):
        slot_contents, predicted_intent = self._command_decoder.decode_text(text)

        print(f"Predicted Intent: {predicted_intent}")
        print("Slot Contents:")
        for slot, content in slot_contents.items():
            print(f"  {slot}: {content}")

        return predicted_intent, slot_contents
