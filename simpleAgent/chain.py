from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import datetime
from langchain_community.tools import TavilySearchResults
from langchain.agents import initialize_agent
from dotenv import load_dotenv

from tools import search_tool, get_date_time

# load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# we can even use from hugging face and llama models

tools = [search_tool, get_date_time]


agent = initialize_agent(llm=llm, tools=tools, agent="zero-shot-react-description", verbose=True)

