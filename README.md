# 🤖 Agentic AI Lab

> **Hands-on experiments for building agentic AI systems** — learning by doing with LangChain, LangGraph, and beyond.

This is my personal lab for learning and experimenting with **agentic AI** — systems where LLMs can reason, use tools, maintain state, and act autonomously. The focus is on **learning by building**: real projects, real code, real experiments.

---

## 🗺️ Learning Map

```
Agentic AI Lab
│
├── ch-langchain/          ← Phase 1: Foundations with LangChain
│   ├── basic-rag              Basic Retrieval-Augmented Generation
│   ├── RAG-faiss              RAG pipeline with FAISS vector store
│   ├── RAG-chromaDB           RAG pipeline with ChromaDB
│   └── fastapi-streamlit-chatbot   Full-stack chatbot (FastAPI + Streamlit)
│
└── ch-langgraph/          ← Phase 2: Agentic workflows with LangGraph
    ├── simple-bot             Basic stateful chatbot with StateGraph
    ├── bot-with-tools         Agent that can call tools
    ├── streaming              Streaming responses from an agent
    └── human-in-loop          Human-in-the-loop approval patterns
```

---

## 📁 Projects

### `ch-langchain/` — LangChain Foundations

| Project | Description | Key Concepts |
|---------|-------------|--------------|
| `basic-rag` | Minimal RAG pipeline — load docs, embed, retrieve, answer | Embeddings, Retrievers, LCEL |
| `RAG-faiss` | RAG with FAISS as the vector store | FAISS, similarity search |
| `RAG-chromaDB` | RAG with ChromaDB as the vector store | ChromaDB, persistent store |
| `fastapi-streamlit-chatbot` | Full-stack chatbot with a FastAPI backend and Streamlit UI | FastAPI, Streamlit, chat history |

### `ch-langgraph/` — LangGraph Agents

| Project | Description | Key Concepts |
|---------|-------------|--------------|
| `simple-bot` | Stateful chatbot built on a `StateGraph` | StateGraph, nodes, edges |
| `bot-with-tools` | Agent that decides when and how to call tools | ToolNode, conditional edges |
| `streaming` | Stream tokens and events from a running agent | `.astream()`, async events |
| `human-in-loop` | Pause graph execution for human approval before proceeding | `interrupt_before`, checkpointing |

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| **LangChain** | LLM abstraction, chains, LCEL |
| **LangGraph** | Stateful agent graph orchestration |
| **FAISS** | Fast local vector similarity search |
| **ChromaDB** | Persistent vector store |
| **FastAPI** | Backend API for chatbot |
| **Streamlit** | Frontend UI for chatbot |
| **OpenAI / Google GenAI** | LLM backends |

---
<p align="center">
  Built with curiosity · Powered by LLMs · One experiment at a time 🧪
</p>
