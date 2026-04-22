import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from database import db
from models import Question
import json

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


def ask(question: Question):
    results = db.query(query_texts=[question.question], n_results=10)
    chunks = results["documents"][0]
    context = "\n".join(chunks)
    print("Context for question:", context)
    prompt = f"""You are a QA engineer assistant. 
        Based on these test cases from our database:
        {context}
        Answer this question: {question.question}"""
    response = llm.invoke(prompt)
    return {"answer": response.content, "source_chunks": chunks}
    
    
    