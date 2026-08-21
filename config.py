import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CVAT_BASE_URL", "https://app.cvat.ai/api")
API_TOKEN = os.getenv("CVAT_PAT")