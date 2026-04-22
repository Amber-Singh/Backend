import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from click import prompt
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from database import add_tests
from models import TestCase, TextInput 
import json
from database import db 

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def get_next_test_id(): #Needs to written by own 
    r = db.get()
    if not r["ids"]:
        return "C_001"
    # Get all test_ids from metadata
    test_ids = [m["test_id"] for m in r["metadatas"]]
    # Get last number
    numbers = [int(tid.split("_")[1]) for tid in test_ids]
    next_num = max(numbers) + 1
    return f"C_{str(next_num).zfill(3)}"

def generate_from_text(input: TextInput):
    prompt = f"""You are a QA engineer. Generate a single API test case based on this description:
    "{input}"

    Return ONLY a valid JSON object with EXACTLY these keys:
    {{
        "test_id": "{get_next_test_id()}",
        "test_name": "...",
        "category": "Happy Path | Negative Path | Validation Error",
        "method": "GET | POST | PUT | DELETE",
        "endpoint": "/api/v1/...",
        "expected_status": 200,
        "request_body": {{}},
        "expected_response": {{}},
        "headers": {{}}
    }}"""
    response = llm.invoke(prompt)
    text_response = response.content
    raw = json.loads(text_response[text_response.find("{"):text_response.rfind("}") + 1]) #conversion of string to python dictionary 
    test = TestCase(**raw)
    add_tests([test.model_dump()])
    return test
