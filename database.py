import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import json
import chromadb


data = json.load(open("api_test_data.json"))["test_cases"]

db = chromadb.PersistentClient("./test_db").get_or_create_collection("api_tests")

# Store
# if db.count() == 0:
#     db.add(
#         ids       = [t["test_id"]   for t in data],
#         documents = [t["test_name"] for t in data],
#         metadatas = [{"category": t["category"], "method": t["method"]} for t in data],
#     )

def chunk_test(test):
    return [
        f"test_id: {test['test_id']}, test_name: {test['test_name']}",
        f"method: {test['method']}, endpoint: {test['endpoint']}",
        f"expected_status: {test['expected_status']}, category: {test['category']}"
    ]

# add to database with chunking
def add_tests(tests):
    ids, documents, metadatas = [], [], []
    for test in tests:
        for i, chunk in enumerate(chunk_test(test)):
            ids.append(f"{test['test_id']}_{i}")
            documents.append(chunk)
            metadatas.append({"category": test["category"], "method": test["method"], 
                              "test_id": test["test_id"]})
    db.add(ids=ids, documents=documents, metadatas=metadatas)
    
# ── Store with chunking
if db.count() == 0:
    add_tests(data)
    print(f"✅ Stored {len(data)} in database with chunking")
    
    
# Get all
def get_all():
    r = db.get()
    for id, doc in zip(r["ids"], r["documents"]):
        print(id, "→", doc)
    return [{"id": i, "name": d, **m} for i, d, m in zip(r["ids"], r["documents"], r["metadatas"])]
        
def get_one(test_id):
    r = db.get(ids=[test_id])
    return {"id": r["ids"][0], "name": r["documents"][0], **r["metadatas"][0]}


#results = db.query(query_texts=["validation error 400"], n_results=3)
#print("Search results for 'validation error 400':",json.dumps(results, indent=2))    

#print(json.dumps(get_all(), indent=2))
#print(json.dumps(db.get(), indent=2))
#get_all()
