from dotenv import load_dotenv
import os


load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")