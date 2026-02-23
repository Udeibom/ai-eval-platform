import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
HF_API_KEY = os.getenv("HF_API_KEY")
HF_GENERATION_MODEL = os.getenv("HF_GENERATION_MODEL")
HF_JUDGE_MODEL = os.getenv("HF_JUDGE_MODEL")