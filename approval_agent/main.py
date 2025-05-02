from langgraph.graph import StateGraph, add_messages, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from langchain.agents import tool
from langchain_community.tools import TavilySearchResults
# from langgraph.types import Command, interrupt


load_dotenv()


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tool = TavilySearchResults()
tools =[tool]

llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    """State of the graph."""

    messages: Annotated[List, add_messages]


def init(state: State):
    """Initialize the state."""
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

def tool_router(state: State):
    last_msf = state["messages"][-1]
    if hasattr(last_msf, "tool_calls") and len(last_msf.tool_calls) > 0:
        return "tools"
    else:
        return END
    

graph = StateGraph(State)

graph.add_node("model", init)
graph.add_node("tools", ToolNode(tools=tools))
graph.set_entry_point("model")

graph.add_conditional_edges("model", tool_router)
graph.add_edge("tools", "model")


app = graph.compile(checkpointer=MemorySaver(), interrupt_before=["tools"])

    
# from IPython.display import Image, display

# display(Image(app.get_graph().draw_mermaid_png()))


config = {"configurable":{
    "thread_id":1
}}

# app.invoke({"messages":[HumanMessage(content="what is the current wether in chennai?")]},config=config)

events = app.stream({
    "messages": [HumanMessage(content="What is the current weather in Chennai?")]
}, config=config, stream_mode="values")

for event in events:
    event["messages"][-1].pretty_print()


print(app.get_state(config=config).next)

print(app.invoke(None, config=config))