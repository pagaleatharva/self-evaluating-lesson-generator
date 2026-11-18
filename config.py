
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize Groq model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

print("Groq model initialized successfully!")
