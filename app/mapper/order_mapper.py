def parse_orders(xml_root):
    orders = []

    headers = xml_root.findall(".//HEADER")
    items = xml_root.findall(".//ITEM")

    def clean_text(value): # json 변환 시 필요없는 공백 없애기 위한 함수
        return value.strip() if value else value

    for header in headers:
        user_id = header.findtext("USER_ID")
        name = header.findtext("NAME")
        address = header.findtext("ADDRESS")
        status = clean_text(header.findtext("STATUS"))

        user_items = [i for i in items if i.findtext("USER_ID") == user_id]

        for item in user_items:
            orders.append({
                "user_id": user_id,
                "name": name,
                "address": address,
                "status": status,
                "item_id": item.findtext("ITEM_ID"),
                "item_name": item.findtext("ITEM_NAME"),
                "price": int(item.findtext("PRICE"))
            })

    return orders