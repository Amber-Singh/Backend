from fastapi import FastAPI
from database import get_all, get_one ,db , add_tests
from models import TestCase
from agents import agent
import json 

app = FastAPI()

@app.get("/tests/all")
def all_tests():
    return get_all()

@app.get("/tests/{test_id}")
def one_test(test_id: str):
    return get_one(test_id)

@app.delete("/tests/{test_id}")
def delete_test(test_id: str):
    db.delete(where={"test_id": test_id})  # ← deletes all chunks automatically ✅
    return {"message": f"Test deleted: {test_id}"}

@app.post("/tests")
def create_test(test: TestCase):
    add_tests([test.model_dump()])  # ← add with chunking
    return {"message": f"Test added: {test.test_id}"}

@app.post("/tests/generate")
def generate_test_cases():
    result = agent.invoke({"existing_tests": [], "generated_tests": []})
    return result["generated_tests"]
 
@app.get("/tests/category/{category}")
def tests_by_Category(category: str):
    result = db.get(where={"category":category})
    return [
        {"id":i, "name":d , **m } for i,d,m in zip(result["ids"], result["documents"], result["metadatas"])
    ]
    
    