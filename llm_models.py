import os
from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def llm_model(model):
    if model == 'OPENAI':
        llm = AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_APIKEY"),
                deployment_name="gpt-4o-mini",
                temperature=0,
                api_version=os.getenv("API_VERSION")
            )
        print("OPENAI")
    else:
        llm= ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                api_key=os.getenv('GEMINI_API_KEY'),
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                # other params...
            )
        print("GEMINI")
    return llm


llm = llm_model(os.getenv("MODEL"))