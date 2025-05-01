from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, add_messages, END


load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class State(TypedDict):
    """State of the graph."""

    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

grpah = StateGraph(State)

grpah.add_node("chatbot", chatbot)
grpah.set_entry_point("chatbot")
grpah.add_edge("chatbot", END)

compiled_graph = grpah.compile()

while True:
    inp = input("User: ")
    if inp == "exit":
        break
    else:
        res = compiled_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=inp),
                ]
            }
        )
        print(res)