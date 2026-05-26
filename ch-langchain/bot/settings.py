import os
from pathlib import Path
from dotenv import load_dotenv

PARENT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = os.path.join(PARENT_DIR,'.env')

load_dotenv(ENV_PATH)


# API Keys
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# LangSmith config
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "tutorial_chat_bot"
