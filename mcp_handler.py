import os, asyncio, json
from fastapi import FastAPI
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

class Query(BaseModel):
    prompt: str

async def run_mcp(prompt: str, job_id: str = None):
    server = StdioServerParameters(command="python", args=["server.py"])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = await session.list_tools()
            tools = [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.inputSchema}} for t in mcp_tools.tools]
            response = llm.bind_tools(tools, tool_choice="auto").invoke([
                SystemMessage(content="You are a helpful assistant. Use tools to answer questions about test cases."),
                HumanMessage(content=prompt)
            ])
            if response.tool_calls:
                tool = response.tool_calls[0]
                result = await session.call_tool(tool["name"], tool["args"])  #
                raw = result.content[0].text
                try:
                    parsed = json.loads(raw)
                except:
                    parsed = raw  # return as plain text if not JSON
                return {"job_id": job_id, "prompt": prompt, "tool_used": tool["name"], "result": parsed}
            return {"job_id": job_id, "prompt": prompt, "answer": response.content}

@app.post("/ask")
async def ask(query: Query):
    return await run_mcp(query.prompt)

# python -m uvicorn test_mcp:app --port 8001 --reload