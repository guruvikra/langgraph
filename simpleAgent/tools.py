from langchain.agents import tool
from datetime import datetime
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

# load_dotenv()
@tool
def get_date_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """returns the current date and time in the specified format."""

    return datetime.now().strftime(format)

search_tool = TavilySearchResults()