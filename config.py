import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR     = os.path.join(BASE_DIR,"data")
RUNBOOK_DIR  = os.path.join(DATA_DIR,"runbooks")
DB_PATH      = os.path.join(DATA_DIR,"incidents.db")
CHROMA_DIR    = os.path.join(DATA_DIR,"chroma_db")