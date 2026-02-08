import socket
import os
from dotenv import load_dotenv

load_dotenv()

try:
    sock = socket.create_connection((os.getenv('ORDER_TB_HOST'), 11527), timeout=5)
    print("MySQL 서버 응답함 ✅")
    sock.close()
except Exception as e:
    print("서버 응답 없음 ❌", e)