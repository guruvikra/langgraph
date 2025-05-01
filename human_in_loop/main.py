# it is a simple example of an agent where i am creaing an post accoring to user input and then i am askinf the user is this post ok if he says ok then i will simple post("here i will simple write post you have to call an api to post") if her says no then ask what to improve and this loop goes on until he says ok.


from typing import Annotated, TypedDict
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, add_messages, END

load_dotenv()



llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class State(TypedDict):
    """State of the graph."""

    messages: Annotated[list, add_messages]


# Define the node names

GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
FEEDBACK = "feedback"

def generate_post(state: State):
    """Generate a post based on user input."""
    # Here you can implement the logic to generate a post
    # For simplicity, we will just return a static post
    return {
        "messages": [llm.invoke(state["messages"])]
    }

def get_review_decision(state: State):
    post = state["messages"][-1].content

    print("-------------------")
    print(post)
    print("-------------------\n")

    decision = input("Is this post ok? (yes/no): ") 
    if decision.lower() =="yes":
        return POST
    else:
        return FEEDBACK
    
def post(state: State):
    print("post posted successfully")


def feedback(state: State):
    feedback = input("What to improve? ")
    return {
        "messages":[llm.invoke([HumanMessage(content=feedback)])]
    }

graph = StateGraph(State)

graph.add_node(GENERATE_POST, generate_post)
graph.add_node(GET_REVIEW_DECISION, get_review_decision)
graph.add_node(POST, post)
graph.add_node(FEEDBACK, feedback)

graph.set_entry_point(GENERATE_POST)
graph.add_conditional_edges(GENERATE_POST,get_review_decision)
graph.add_edge(POST, END)
graph.add_edge(FEEDBACK, GENERATE_POST)
compiled_graph = graph.compile()


res =  compiled_graph.invoke({
    "messages": [
        HumanMessage(content="Create a post about AI and its impact on society.")
    ]
})