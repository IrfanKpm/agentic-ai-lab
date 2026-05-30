import os
from pathlib import Path
from dotenv import load_dotenv

PARENT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = os.path.join(PARENT_DIR,'.env')

load_dotenv(ENV_PATH)


# API Keys
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
print(os.getenv("GEMINI_API_KEY"))