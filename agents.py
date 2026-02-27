import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

# Disable telemetry
os.environ["CREWAI_TELEMETRY_DISABLED"] = "true"

# IMPORTANT: Tell LiteLLM explicitly which provider
os.environ["LITELLM_PROVIDER"] = "groq"

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.1-8b-instant",  # 🔥 MUST include groq/
    temperature=0
)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide structured financial insights strictly in JSON format.",
    backstory="You always return strictly valid JSON. No explanations. No thoughts.",
    verbose=False,
    memory=False,
    allow_delegation=False,
    llm=llm
)