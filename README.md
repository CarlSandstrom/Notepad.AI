# Notepad.AI
This is a very simple notepad clone with the important difference that it has a built in copilot. It is mainly for educational purposes.

## Prerequisites
Create a virtual environment 

`python3 -m venv venv`

Activate the virtual environment

`. venv/bin/activate`

Install required packages

`pip install PyQt5 torch transformers scikit-learn numpy matplotlib appdirs`

## Training the model

First, the model needs to be trained. It is a simple procedure where the model is fed sentences/commands and the meaning of the command. This tunes the model to understand the commands. The reason that the user has to train the is simply because the files are a bit too large to be stored on Github. The training is performed by running the script Trainer.py

`cd ai/training`
`python Trainer.py`

the models are stored in `ai/models`.

## Running Notepad.AI

From the virtual environment, simply run `gui/main.py`