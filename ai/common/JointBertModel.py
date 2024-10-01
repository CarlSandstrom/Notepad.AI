from transformers import BertModel, BertConfig
from torch import nn
import torch


class JointBertModel(nn.Module):
    def __init__(self, num_intents, num_slots):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.dropout = nn.Dropout(0.1)
        self.intent_classifier = nn.Linear(self.bert.config.hidden_size, num_intents)
        self.slot_classifier = nn.Linear(self.bert.config.hidden_size, num_slots)

    def forward(self, input_ids, attention_mask, intent_labels=None, slot_labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        
        sequence_output = self.dropout(outputs.last_hidden_state)
        pooled_output = self.dropout(outputs.pooler_output)

        intent_logits = self.intent_classifier(pooled_output)
        slot_logits = self.slot_classifier(sequence_output)

        loss = None
        if intent_labels is not None and slot_labels is not None:
            intent_loss = nn.CrossEntropyLoss()(intent_logits, intent_labels)
            slot_loss = nn.CrossEntropyLoss()(slot_logits.view(-1, self.slot_classifier.out_features), slot_labels.view(-1))
            loss = intent_loss + slot_loss

        return slot_logits, intent_logits, loss

    def save_model(self, save_directory):
        # Save the BERT part using save_pretrained
        self.bert.save_pretrained(save_directory)

        # Save the classifiers and any other custom parts
        torch.save(
            {
                "intent_classifier": self.intent_classifier.state_dict(),
                "slot_classifier": self.slot_classifier.state_dict(),
            },
            f"{save_directory}/classifiers.pth",
        )

    @classmethod
    def load_model(cls, save_directory, num_intents, num_slots):
        # Load the BERT part
        bert = BertModel.from_pretrained(save_directory)

        # Initialize the full model
        model = cls(num_intents, num_slots)
        model.bert = bert

        # Load the classifiers
        classifiers_data = torch.load(f"{save_directory}/classifiers.pth")
        model.intent_classifier.load_state_dict(classifiers_data["intent_classifier"])
        model.slot_classifier.load_state_dict(classifiers_data["slot_classifier"])

        return model
