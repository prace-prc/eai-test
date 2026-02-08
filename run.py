import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('ORDER_TB_HOST'), os.getenv('ORDER_TB_PORT'), os.getenv('ORDER_TB_SID'))