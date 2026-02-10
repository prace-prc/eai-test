import json
from datetime import datetime
import os

OUTPUT_DIR = "output"

def save_orders_to_file(orders):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/orders_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

    return filename