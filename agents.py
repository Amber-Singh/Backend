import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from database import get_all, add_tests, db
import json

load_dotenv()

# ── LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
 
 # ── State
class State(TypedDict):
    existing_tests: List[dict]
    generated_tests: List[dict]
    
# ── Node 1: Load
def load_tests(state: State) -> State:
    print("\n── NODE: load ──")
    print("State IN :", state)
    state["existing_tests"] = get_all()
    print("State OUT:", {"existing_tests": f"{len(state['existing_tests'])} tests loaded", "generated_tests": []})
    return state

def generate_tests(state: State) -> State:
    print("\n── NODE: generate ──")
    print("State IN :", {"existing_tests": f"{len(state['existing_tests'])} tests", "generated_tests": []})
    # Generate new tests based on existing ones
    # For simplicity, we just create dummy tests here   
    prompt = f"""You are a QA engineer. Based on these existing API test cases:
            {json.dumps(state["existing_tests"][-5:], indent=2)}

            Generate 3 NEW test cases not already covered.
            Return ONLY a valid JSON array. Use EXACTLY these key names:
            [
                {{
                    "test_id": "C_011",
                    "test_name": "...",
                    "category": "Happy Path | Negative Path | Validation Error",
                    "method": "GET | POST | PUT | DELETE",
                    "endpoint": "/api/v1/...",
                    "expected_status": 200,
                    "request_body": {{}},
                    "expected_response": {{}},
                    "headers": {{}}
                }}
            ]"""
    response = llm.invoke(prompt)
    text = response.content
    state["generated_tests"] = json.loads(text[text.find("["):text.rfind("]") + 1])
    return state

def save_tests(state: State) -> State:
    print("\n── NODE: save ──")
    print("State IN :", {"existing_tests": f"{len(state['existing_tests'])} tests", "generated_tests": f"{len(state['generated_tests'])} tests"})
    # Save generated tests to DB
    add_tests(state["generated_tests"])   # ← calling add_tests with generated tests
    print("State OUT: saved to ChromaDB ✅")
    return state
    

graph = StateGraph(State)
graph.add_node(load_tests)
graph.add_node(generate_tests)
graph.add_node(save_tests)

graph.set_entry_point("load_tests")
graph.add_edge("load_tests", "generate_tests")
graph.add_edge("generate_tests", "save_tests")      
graph.add_edge("save_tests", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"existing_tests": [], "generated_tests": []})
    print(json.dumps(result["generated_tests"], indent=2))