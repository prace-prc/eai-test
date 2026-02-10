import base64

def decode_base64_euckr(data: str) -> str:
    try:
        decoded_bytes = base64.b64decode(data)
        return decoded_bytes.decode("euc-kr")
    except Exception as e:
        raise ValueError(f"디코딩 실패: {e}")