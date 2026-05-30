from pathlib import Path
import json


DATA_FILE = Path(__file__).resolve().parent / "NozzleData.json"


with open(DATA_FILE, "r", encoding="utf-8") as f:
    NOZZLE_DATA = json.load(f)
