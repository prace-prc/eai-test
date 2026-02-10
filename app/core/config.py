import os
from dotenv import load_dotenv

load_dotenv()

APPLICANT_KEY = os.getenv("APPLICANT_KEY")
APPLICANT_NAME = os.getenv("APPLICANT_NAME")