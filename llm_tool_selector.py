# llm_decider.py
from fastapi import FastAPI
import uvicorn
import httpx

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LLM Decider Running", "usage": "GET /decide?prompt=your prompt here"}

@app.get("/decide")
def decide(prompt: str):
    p = prompt.lower()
    
    # Decide which tool to use
    if "c_" in p and ("get" in p or "fetch" in p):
        # Extract ID
        words = p.split()
        test_id = next((w for w in words if 'c_' in w), "C_009_2").upper()
        return {"tool": "get_test_by_id", "params": {"test_id": test_id}, "prompt": prompt}
    
    elif "delete" in p or "remove" in p:
        words = p.split()
        test_id = next((w for w in words if 'c_' in w), "C_011_2").upper()
        return {"tool": "delete_test", "params": {"test_id": test_id}, "prompt": prompt}
    
    elif "search" in p or "find" in p:
        query = p.replace("search", "").replace("find", "").replace("for", "").strip()
        if not query:
            query = "401"
        return {"tool": "search_tests", "params": {"query": query}, "prompt": prompt}
    
    elif "category" in p or "path" in p:
        if "happy" in p:
            category = "Happy Path"
        elif "negative" in p:
            category = "Negative Path"
        elif "positive" in p:
            category = "Positive Path"
        else:
            category = "Happy Path"
        return {"tool": "get_tests_by_category", "params": {"category": category}, "prompt": prompt}
    
    else:
        return {"tool": "list_all_tests", "params": {}, "prompt": prompt}

@app.get("/execute")
def execute(prompt: str):
    """Decide AND execute the tool"""
    decision = decide(prompt)
    
    tool = decision["tool"]
    params = decision["params"]
    
    # Call the actual FastAPI backend
    if tool == "list_all_tests":
        response = httpx.get("http://localhost:8000/tests/all")
    elif tool == "get_test_by_id":
        response = httpx.get(f"http://localhost:8000/tests/{params['test_id']}")
    elif tool == "search_tests":
        response = httpx.get(f"http://localhost:8000/tests/search/{params['query']}")
    elif tool == "get_tests_by_category":
        response = httpx.get(f"http://localhost:8000/tests/category/{params['category']}")
    elif tool == "delete_test":
        response = httpx.delete(f"http://localhost:8000/tests/{params['test_id']}")
    else:
        response = None
    
    return {
        "decision": decision,
        "result": response.json() if response else {"error": "No result"}
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)