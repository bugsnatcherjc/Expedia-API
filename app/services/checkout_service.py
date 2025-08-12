import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

class CheckoutService:
    def _load(self, name: str):
        with open(DATA_DIR / f"{name}.json", encoding="utf-8") as f:
            return json.load(f)

    def get_checkout(self):
        return self._load("checkout_data")