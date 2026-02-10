from app.utils.id_generator import generate_order_id
def parse_orders(xml_root, session):
    orders = []

    prefix, number = generate_order_id(session)

    headers = xml_root.findall(".//HEADER")
    items = xml_root.findall(".//ITEM")

    def clean_text(value): # XML에서 변환 시 필요없는 공백 없애기 위한 함수
        return value.strip() if value else value

    for header in headers:
        user_id = header.findtext("USER_ID")
        name = header.findtext("NAME")
        address = header.findtext("ADDRESS")
        status = clean_text(header.findtext("STATUS"))

        user_items = [i for i in items if clean_text(i.findtext("USER_ID")) == user_id]

        for item in user_items:
            number += 1
            if number > 999:
                prefix = chr(ord(prefix) + 1)
                number = 1

            order_id = f"{prefix}{number:03d}"

            orders.append({
                "order_id": order_id,
                "user_id": user_id,
                "name": name,
                "address": address,
                "status": status,
                "item_id": clean_text(item.findtext("ITEM_ID")),
                "item_name": clean_text(item.findtext("ITEM_NAME")),
                "price": int(clean_text(item.findtext("PRICE")))
            })

    return orders