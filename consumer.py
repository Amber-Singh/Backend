import os, asyncio, json, time
from kafka import KafkaConsumer, KafkaProducer
from mcp_handler import run_mcp  # ← import shared logic

consumer = KafkaConsumer("test-requests", bootstrap_servers="kafka:9092",  auto_offset_reset="earliest",  
                         value_deserializer=lambda v: json.loads(v.decode("utf-8")))
producer = KafkaProducer(bootstrap_servers="kafka:9092", 
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))

print("✅ Consumer started! Waiting for messages...")
for message in consumer:
    job_id = message.value["job_id"]
    prompt = message.value["prompt"]
    print(f"\n📩 Received job {job_id}: {prompt}")
    try:
        time.sleep(2)
        result = asyncio.run(run_mcp(prompt, job_id))  # ← use shared logic
        producer.send("test-responses", result)
        producer.flush()
        print("📤 Sent to test-responses topic")
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"❌ FULL ERROR:\n{err}", flush=True)
        producer.send("test-responses", {"job_id": job_id, "status": "error", "message": err})
        producer.flush()