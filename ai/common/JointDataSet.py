import torch
from torch.utils.data import Dataset


class JointDataSet(Dataset):
    def __init__(self, encoded_data):
        self.encoded_data = encoded_data

    def __len__(self):
        return len(self.encoded_data)

    def __getitem__(self, idx):
        item = self.encoded_data[idx]
        return {
            "input_ids": torch.tensor(item["input_ids"]),
            "attention_mask": torch.tensor(item["attention_mask"]),
            "intent": torch.tensor(item["intent"]),
            "slot_labels": torch.tensor(item["slot_labels"]),
        }
