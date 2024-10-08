import sys

sys.path.append("/home/carl/dev/Notepad.AI/")

import torch
from ai.common.Constants import *
from ai.common.JointBertModel import JointBertModel
from transformers import AutoTokenizer


class CommandDecoder:
    def __init__(self):
        num_intents = len(labels_mapping)
        num_slots = len(slotId_to_str_mapping)
        self.model = JointBertModel.load_model(
            "ai/models/",
            num_intents=num_intents,
            num_slots=num_slots,
        )
        self.model.eval()

        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def decode_text(self, input_text):
        # Tokenize the input
        encoded = self.tokenizer.encode_plus(
            input_text, return_offsets_mapping=True, add_special_tokens=True, return_tensors="pt"
        )
        input_ids = encoded["input_ids"]
        attention_mask = encoded["attention_mask"]
        offset_mapping = encoded["offset_mapping"][0]

        # Get model predictions
        with torch.no_grad():
            slot_logits, intent_logits, _ = self.model(input_ids, attention_mask)

        # Get the predicted slot labels
        predicted_slot_ids = torch.argmax(slot_logits[0], dim=1)
        predicted_slot_labels = [slotId_to_str_mapping[id.item()] for id in predicted_slot_ids]

        # Align labels with original text
        aligned_labels = []
        for i, (start, end) in enumerate(offset_mapping):

            if start == end == 0:  # Special tokens
                aligned_labels.append("O")
            else:
                aligned_labels.append(predicted_slot_labels[i])

        # Extract slots based on aligned labels
        slot_contents = {}
        current_slot = None
        start_index = 0

        for i, (label, (start, end)) in enumerate(zip(aligned_labels, offset_mapping)):
            if label == "O":
                start_index = end
                continue

            current_slot = label[2:]
            if not (current_slot in slot_contents.keys()):
                slot_contents[current_slot] = ""

            slot_contents[current_slot] += input_text[start_index:end]
            start_index = end

        # Get predicted intent
        predicted_intent_id = torch.argmax(intent_logits, dim=1).item()
        predicted_intent = labels_mapping[predicted_intent_id]

        return labels_mapping_inv[predicted_intent], slot_contents


if __name__ == "__main__":
    decoder = CommandDecoder()

    input_text = 'Please replace "old puggle knoff" with "new shmuck schmakk dinke plojj 999. XYZ"'  # 'Save this document as "notes_21.csv"'
    predicted_intent, slot_contents = decoder.decode_text(input_text)
    print(f"Predicted Intent: {predicted_intent}")
    print("Slot Contents:")
    for slot, content in slot_contents.items():
        print(f"  {slot}: {content}")
