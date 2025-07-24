import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("JOTFORM_API_KEY")
FORM_ID = os.getenv("JOTFORM_FORM_ID")
BASE_URL = "https://api.jotform.com"

# Validates environment variables 
def validate_config():
    if not API_KEY or not FORM_ID:
        raise EnvironmentError("Missing JOTFORM_API_KEY or JOTFORM_FORM_ID in .env")
