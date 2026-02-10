from datetime import datetime
import os

OUTPUT_DIR = "output"

def save_orders_to_file(orders, applicant_name, applicant_id):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{OUTPUT_DIR}/INSPIEN_{applicant_name}_{timestamp}.txt"

    lines = []
    for o in orders:
        line = "^".join([
            o["order_id"],
            o["user_id"],
            o["item_id"],
            applicant_id,
            o["name"],
            o["address"],
            o["item_name"],
            str(o["price"])
            ]) + "\\" + o["status"].lower()
        
        lines.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return filename