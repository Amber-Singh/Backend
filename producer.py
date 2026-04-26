import os, json, uuid
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaConsumer as KC
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

class Query(BaseModel):
    prompt: str

# Step 1 - User hits /ask, gets job_id back immediately
@app.post("/ask")
def ask(query: Query):
    job_id = str(uuid.uuid4())  # generate unique job id
    producer.send("test-requests", {"job_id": job_id, "prompt": query.prompt})
    producer.flush()
    return {"job_id": job_id, "message": "Request received! Use job_id to get result."}

# Step 2 - User polls /result/{job_id} to get result
@app.get("/result/{job_id}")
def get_result(job_id: str):
    c = KC(
        "test-responses",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        consumer_timeout_ms=3000,  # wait max 3 seconds
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    # Search all messages for matching job_id
    for message in c:
        if message.value.get("job_id") == job_id:
            c.close()
            return message.value  # found it!

    c.close()
    return {"status": "pending", "message": "Result not ready yet, try again!"}

# uvicorn producer:app --port 8001 --reload