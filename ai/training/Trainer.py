import sys

sys.path.append("/home/carl/dev/Notepad.AI/")

from TrainerData import trainingData
from DataEncoder import DataEncoder
from ai.common.JointBertModel import JointBertModel
from ai.common.JointDataSet import JointDataSet
import ai.common.Constants as Constants

from transformers import AutoTokenizer
from torch.utils.data import DataLoader
import torch
from torch import nn

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

encoded_data = [DataEncoder(tokenizer, dataItem).getEncodedData() for dataItem in trainingData]

# Get the number of unique intents and slots
num_intents = max(dataItem["intent"] for dataItem in trainingData) + 1
num_slots = len(Constants.slotId_to_str_mapping)

print(f"Number of intents: {num_intents}")
print(f"Number of slots: {num_slots}")

model = JointBertModel(num_intents=num_intents, num_slots=num_slots)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

dataset = JointDataSet(encoded_data)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

intent_criterion = nn.CrossEntropyLoss()
slot_criterion = nn.CrossEntropyLoss(ignore_index=-100)

num_epochs = 400

for epoch in range(num_epochs):
    total_loss = 0
    for batch in dataloader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        intent_labels = batch["intent"].to(device)
        slot_labels = batch["slot_labels"].to(device)

        slot_logits, intent_logits, loss = model(input_ids, attention_mask, intent_labels, slot_labels)

        total_loss += loss.item()

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{num_epochs} completed. Average loss: {avg_loss}")

    if avg_loss < 0.01:
        break

print("Training completed.")

# Save the model
model.save_model("ai/models")
