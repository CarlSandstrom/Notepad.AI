# Labels
SAVE_FILE = 0
OPEN_FILE = 1
EXIT_PROGRAM = 2
COPY_TEXT = 3
PASTE_TEXT = 4
REPLACE = 5

# Define a mapping from class indices to labels
labels_mapping = {
    SAVE_FILE: "SAVE_FILE",
    OPEN_FILE: "OPEN_FILE",
    EXIT_PROGRAM: "EXIT_PROGRAM",
    COPY_TEXT: "COPY_TEXT",
    PASTE_TEXT: "PASTE_TEXT",
    REPLACE: "REPLACE",
}

labels_mapping_inv = {v: k for k, v in labels_mapping.items()}

# Slots
O = 0
B_FILENAME = 1
I_FILENAME = 2
B_SEARCH_TERM = 3
I_SEARCH_TERM = 4
B_REPLACE_TERM = 5
I_REPLACE_TERM = 6
B_QUOTE = 7
E_QUOTE = 8

slotId_to_str_mapping = {
    O: "O",
    B_FILENAME: "B-FILENAME",
    I_FILENAME: "I-FILENAME",
    B_SEARCH_TERM: "B-SEARCH_TERM",
    I_SEARCH_TERM: "I-SEARCH_TERM",
    B_REPLACE_TERM: "B-REPLACE_TERM",
    I_REPLACE_TERM: "I-REPLACE_TERM",
    B_QUOTE: "B-QUOTE",
    E_QUOTE: "E-QUOTE",
}

slotStr_to_Id_mapping = {v: k for k, v in slotId_to_str_mapping.items()}
