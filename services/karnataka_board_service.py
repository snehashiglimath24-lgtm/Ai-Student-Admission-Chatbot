import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "eligibility_rules.json"

def load_board_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

BOARD_DATA = load_board_data()

def get_board_overview(board_key):
    return BOARD_DATA.get(board_key.lower())

def get_kcet_info():
    return get_board_overview("kcet")

def get_comedk_info():
    return get_board_overview("comedk")
