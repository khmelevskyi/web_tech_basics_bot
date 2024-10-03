import os
import json
from enum import Enum


directory_path = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
new_path = os.path.join(directory_path, "text.json")

with open(new_path, "r", encoding="utf-8") as fp:
    text = json.load(fp)


class States(Enum):

    MAIN_MENU = 0

    CHATGPT = 1
