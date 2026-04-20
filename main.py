from fastapi import FastAPI
from database import get_all, get_one

app = FastAPI()

@app.get("/tests")
def all_tests():
    return get_all()

@app.get("/tests/{test_id}")
def one_test(test_id: str):
    return get_one(test_id)