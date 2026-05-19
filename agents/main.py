from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools.retriever import create_retriever_tool
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain_core.documents import Document

from langchain.agents import create_agent

import os
import settings


# src1
api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=200
)

wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

#result = wiki_tool.run("LangChain")
#print(result)


# src2
gfg_url = "https://www.geeksforgeeks.org/artificial-intelligence/agents-artificial-intelligence/"

loader = WebBaseLoader(gfg_url)
docs = loader.load()


# Saving webpage text locally avoids downloading
# the webpage repeatedly in future runs.
#
# This improves startup speed significantly.
with open("ai_agents.txt", "w", encoding="utf-8") as file:
    file.write(docs[0].page_content)

# Large documents are inefficient for embeddings.
# Smaller chunks improve:
# - retrieval accuracy
# - memory efficiency
# - search speed
#
# Optimization:
# Reduced chunk_size from 1000 -> 500
# Reduced overlap from 200 -> 50

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Convert webpage into smaller text chunks
documents = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Creating embeddings every run is expensive.
#
# Optimization:
# Save FAISS database locally and reload it later.
#
# First Run:
# - Create embeddings
# - Build FAISS index
# - Save locally
#
# Later Runs:
# - Load FAISS directly
# - Skip embedding generation
#
# This is the BIGGEST performance optimization.

FAISS_DB_PATH = "faiss_index"
# Check if FAISS index already exists
if os.path.exists(FAISS_DB_PATH):

    # Load existing FAISS index
    vectorDB = FAISS.load_local(
        FAISS_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS index loaded from disk.")

else:

    # Create FAISS vector database
    vectorDB = FAISS.from_documents(
        documents,
        embeddings
    )

    # Save FAISS database locally
    vectorDB.save_local(FAISS_DB_PATH)
    print("FAISS index created and saved.")


# Retriever searches vector database for
# semantically relevant chunks.
#
# Optimization:
# k=2 means retrieve only top 2 chunks.
#
# Benefits:
# - faster retrieval
# - lower token usage
# - faster LLM response

retriever = vectorDB.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)

# Agents can now use this tool automatically.

retriever_tool = create_retriever_tool(
    retriever,
    # Tool name
    "ai_agents_tool",
    # Tool description
    """
    Use this tool for Artificial Intelligence Agents concepts.

    Includes:
    - What are AI agents
    - Types of agents in AI
    - Agent architectures
    - Goal-based agents
    - Utility-based agents
    - Learning agents
    - Real-world agent applications
    """
)

# Query the retriever tool
#response = retriever_tool.invoke("What are AI agents?")
#print(response)

#src3
arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=3,
    doc_content_chars_max=4000
)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
#arxiv_result = arxiv_tool.run("Large Language Models")

tools = [wiki_tool, retriever_tool, arxiv_tool]

# 2. Correctly initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

# 3. Create the LangGraph-powered compiled agent
agent = create_agent(
    model=llm, 
    tools=tools,
    system_prompt="You are a research assistant. Use Wikipedia, the retriever, or ArXiv to provide accurate answers."
)


query = "Compare the architecture of a Simple Reflex Agent and a Learning Agent..."
response_state = agent.invoke({"messages": [{"role": "user", "content": query}]})
print(response_state["messages"][-1].content)
