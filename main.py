from fastapi import FastAPI
from database import get_all, get_one ,db , add_tests
from models import TestCase , TextInput , Question
from agents import agent
from fastapi.responses import FileResponse
from text_agent import generate_from_text
from rag import ask
import json, os

app = FastAPI()

@app.get("/tests/all")
def all_tests():
    return get_all()

@app.get("/tests/export")
def export_tests():
    result = get_all()
    with open("exported_tests.json", "w") as f:
        json.dump(result, f, indent=2)
    return FileResponse("exported_tests.json", media_type="application/json", filename="exported_tests.json")

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

@app.put("/tests/{test_id}")
def update_test(test_id: str, test: TestCase):
    # Delete old test
    db.delete(where={"test_id": test_id})
    # Add updated test
    add_tests([test.model_dump()])
    return {"message": f"Test updated: {test_id}"}
    
@app.get("/tests/search/{query}")
def search_tests(query: str, int =3):
    result = db.query(query_texts=[query], n_results=int)
    return [
        {"id":i, "name":d , **m , "distance": dist} for i,d,m,dist in zip(result["ids"][0], 
        result["documents"][0], result["metadatas"][0], result["distances"][0])
    ]

@app.post("/tests/generate-from-text")
def generate_from_text_endpoint(input:TextInput):
    return generate_from_text(input.text)


@app.post("/tests/ask")
def ask_endpoint(question: Question):
    return ask(question)