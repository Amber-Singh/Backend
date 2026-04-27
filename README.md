# Test Case Management API

A FastAPI-based backend service for managing test cases with vector search capabilities using ChromaDB. This API allows you to create, read, update, delete, and semantically search test cases, with AI-powered test case generation.

## 🚀 Features

- **CRUD Operations**: Create, read, update, and delete test cases
- **Semantic Search**: Find similar test cases using vector embeddings
- **AI Generation**: Automatically generate test cases using AI agents
- **Category Filtering**: Retrieve test cases by category
- **Export Functionality**: Export all test cases to JSON format
- **Vector Database**: Uses ChromaDB for efficient similarity search

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <your-repository-url>
cd backend
=====================================================================================================
# 🤖 AI Test Case Manager

An intelligent backend system for managing, generating, and querying test cases using AI agents, RAG, MCP, and async Kafka messaging.

---

## 🏗️ Architecture

```
User → POST /ask → Redpanda Kafka → Consumer → MCP → Groq LLM → Tool Call → Response
```

**Stack:** FastAPI · LangGraph · LangChain · Groq (LLaMA 3.3) · ChromaDB · MCP · Kafka (Redpanda) · Docker · Railway

---

## 🌐 Live URLs

| Service | URL |
|---|---|
| Main API | `https://backend-production-95de.up.railway.app/docs` |
| Producer API | `https://bubbly-learning-production-cdba.up.railway.app/docs` |

---

## 📡 Endpoints

### Main App — Test Case Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tests/all` | Get all test cases |
| GET | `/tests/{test_id}` | Get test case by ID |
| GET | `/tests/export` | Export tests as JSON |
| GET | `/tests/search/{query}` | Search by keyword |
| GET | `/tests/category/{category}` | Filter by category |
| POST | `/tests` | Create a test case |
| POST | `/tests/generate` | Auto-generate via AI agent |
| POST | `/tests/generate-from-text` | Generate from plain text |
| POST | `/tests/ask` | Ask a question using RAG |
| PUT | `/tests/{test_id}` | Update a test case |
| DELETE | `/tests/{test_id}` | Delete a test case |

### Producer App — Async AI Query

| Method | Endpoint | Description |
|---|---|---|
| POST | `/ask` | Submit prompt → returns `job_id` |
| GET | `/result/{job_id}` | Poll for result |

---

## ⚙️ Local Setup

```bash
git clone https://github.com/Amber-Singh/Backend.git
cd Backend

# Add .env file
cp .env.example .env  # fill in your keys

# Run with Docker
docker-compose up --build
```

### Required ENV Variables

```
GROQ_API_KEY=
KAFKA_BOOTSTRAP_SERVERS=
KAFKA_USERNAME=
KAFKA_PASSWORD=
```

---

## 🗂️ Project Structure

```
├── main.py          # FastAPI - Test case CRUD + RAG
├── producer.py      # FastAPI - Async Kafka producer
├── consumer.py      # Kafka consumer - processes jobs
├── mcp_handler.py   # MCP client + Groq LLM
├── server.py        # MCP server with tools
├── agents.py        # LangGraph AI agents
├── rag.py           # RAG implementation
├── database.py      # ChromaDB vector store
├── Dockerfile
└── docker-compose.yml
```

---

## 🚀 Deployment

- **Kafka:** Redpanda Serverless (cloud)
- **Services:** Railway (auto-deploy from GitHub)