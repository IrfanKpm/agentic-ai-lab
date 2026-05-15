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
import settings


# src1
api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=200
)

wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

result = wiki_tool.run("LangChain")
print(result)


# src2
gfg_url = "https://www.geeksforgeeks.org/artificial-intelligence/agents-artificial-intelligence/"

loader = WebBaseLoader(gfg_url)
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorDB = FAISS.from_documents(documents, embeddings)
retriever = vectorDB.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "ai_agents_tool",
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

response = retriever_tool.invoke("What are AI agents?")
print(response)

#src3
arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=3,
    doc_content_chars_max=4000
)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)

arxiv_result = arxiv_tool.run("Large Language Models")

tools = [wiki_tool,retriever_tool,arxiv_tool]
print(tools)