import re
from transformers import AutoTokenizer
import ai.common.Constants as Constants

class DataEncoder:
    def __init__(self, tokenizer, dataItem):
        self.tokenizer = tokenizer
        self.dataItem = dataItem
        self._encodedData = self._encodeData()

    def _encodeData(self):
        text = self.dataItem["text"]
        slots = self.dataItem["slots"]
        slots_inverse = {slots[a]: a for a in slots}

        # Tokenize the input
        tokenized = self.tokenizer(
            text, 
            padding="max_length", 
            truncation=True, 
            max_length=64,
            return_offsets_mapping=True
        )

        # Create slot labels
        slot_labels = ['O'] * len(tokenized['input_ids'])

        # Find quoted strings and their positions
        quoted_strings = re.finditer(r'"([^"]*)"', text)
        for match in quoted_strings:
            slot_value = match.group(1)
            if slot_value in slots_inverse:
                start, end = match.span()  # span including quotes
                slot_type = slots_inverse[slot_value]

                # Find corresponding tokens
                in_slot = False
                for i, (token_start, token_end) in enumerate(tokenized.offset_mapping):
                    if token_start >= start and token_end <= end:
                        if token_start == start:
                            slot_labels[i] = 'B-QUOTE'
                        elif token_end == end:
                            slot_labels[i] = 'E-QUOTE'
                        elif not in_slot:
                            slot_labels[i] = f'B-{slot_type}'
                            in_slot = True
                        else:
                            slot_labels[i] = f'I-{slot_type}'

        # Convert slot labels to IDs
        slot_ids = [Constants.slotStr_to_Id_mapping [label] for label in slot_labels]

        return {
            "input_ids": tokenized["input_ids"],
            "attention_mask": tokenized["attention_mask"],
            "intent": self.dataItem["intent"],
            "slot_labels": slot_ids,
        }

    def getEncodedData(self):
        return self._encodedData