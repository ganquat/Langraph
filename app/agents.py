import os
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# Ensure the API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")

# Initialize the Gemini model
# Note: Adjust model_name if needed, e.g., "gemini-1.5-flash"
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=api_key)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str # To indicate which agent to route to next

# Define a simple tool (can be expanded)
def simple_search(query: str) -> str:
    """A simple search tool that returns a placeholder result."""
    return f"Search results for '{query}': This is a placeholder. Implement actual search logic here."

# Agent 1: Researcher
def researcher_agent(state: AgentState):
    """Agent responsible for gathering initial information."""
    messages = state['messages']
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a researcher. Your task is to understand the user's query and gather initial information. If the query is about a specific topic, perform a search."),
        ("human", "{input}")
    ])
    chain = prompt | llm
    response = chain.invoke({"input": messages[-1].content}) # Use the latest human message

    # Simulate using the search tool if relevant (simple keyword check)
    if "search for" in messages[-1].content.lower() or "find information on" in messages[-1].content.lower():
        search_query = messages[-1].content.split("search for")[-1].split("find information on")[-1].strip()
        tool_result = simple_search(search_query)
        response_content = f"{response.content}\n\n{tool_result}"
    else:
        response_content = response.content

    return {"messages": [HumanMessage(content=response_content)], "next_node": "planner"}

# Agent 2: Planner
def planner_agent(state: AgentState):
    """Agent responsible for creating a plan based on research."""
    messages = state['messages']
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a planner. Based on the information provided, create a step-by-step plan to address the user's request."),
        ("human", "Given the following information:\n{info}\n\nCreate a plan.")
    ])
    chain = prompt | llm
    # Combine previous messages to form the 'info' for the planner
    info_for_planner = "\n".join([msg.content for msg in messages])
    response = chain.invoke({"info": info_for_planner})
    return {"messages": [HumanMessage(content=response.content)], "next_node": "final_responder"}

# Agent 3: Final Responder (could also be a synthesizer or executor)
def final_responder_agent(state: AgentState):
    """Agent responsible for synthesizing the information and providing the final response."""
    messages = state['messages']
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the final responder. Synthesize all the information and plans created by other agents and provide a comprehensive answer to the initial user query."),
        ("human", "Based on the following conversation and plan:\n{conversation}\n\nProvide a final, user-facing response.")
    ])
    chain = prompt | llm
    conversation_history = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in messages])
    response = chain.invoke({"conversation": conversation_history})
    return {"messages": [HumanMessage(content=response.content)], "next_node": END}


# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_agent)
workflow.add_node("planner", planner_agent)
workflow.add_node("final_responder", final_responder_agent)

# Define edges
workflow.set_entry_point("researcher")

def route_logic(state: AgentState):
    return state['next_node']

workflow.add_conditional_edges(
    "researcher",
    route_logic,
    {"planner": "planner", END: END} # Should always go to planner from researcher in this simple setup
)
workflow.add_conditional_edges(
    "planner",
    route_logic,
    {"final_responder": "final_responder", END: END} # Should always go to final_responder from planner
)
workflow.add_edge("final_responder", END)


# Compile the graph
app_graph = workflow.compile()

# Function to run the graph (for Flask app to call)
def run_graph(user_input: str):
    initial_state = {"messages": [HumanMessage(content=user_input)], "next_node": "researcher"}
    # The input to app.invoke must match the AgentState structure
    # We pass the initial messages which will be processed by the entry point (researcher)
    final_state = app_graph.invoke(initial_state)
    return final_state['messages'][-1].content

if __name__ == '__main__':
    # Example usage (for testing this script directly)
    print("Testing agents.py...")
    print("\n--- Running Graph with a simple query ---")
    output = run_graph("Tell me about Large Language Models.")
    print(f"Final Output:\n{output}")

    print("\n--- Running Graph with a query requiring search ---")
    output_search = run_graph("Can you search for information on the LangGraph library?")
    print(f"Final Output:\n{output_search}")
