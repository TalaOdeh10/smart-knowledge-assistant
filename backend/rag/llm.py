import os

from dotenv import load_dotenv#s a zero-dependency module that loads environment variables from a .env file into your application's environment

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )