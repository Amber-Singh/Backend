from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
import os
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

prompt = ChatPromptTemplate.from_template(
    "You are a QA engineer. Answer this: {question}"
)


# chain = prompt | llm | StrOutputParser()
# response = chain.invoke({"question": "what is a test case?"})
# print(response)

# json_prompt = ChatPromptTemplate.from_template(
#     """Generate a test case as JSON only, no extra text:
#     {{
#         "test_id": "C_001",
#         "test_name": "...",
#         "category": "Happy Path"
#     }}
#     Description: {description}"""
# )

# chain = json_prompt | llm | JsonOutputParser()
# response = chain.invoke({"description": "A simple login test"})
# print(response)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a QA engineer assistant."),
    MessagesPlaceholder(variable_name="history"),  # ← memory goes here
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

history = []

def chat(question):
    response = chain.invoke({
        "question": question,
        "history": history
    })
    # Add to history
    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=response))
    return response

print(chat("what is a test case?"))
print(chat("give me an example of what I just asked"))  # ← remembers! ✅
print(chat("now make it a negative test case"))