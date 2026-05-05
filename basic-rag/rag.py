import settings

import bs4
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from playwright.sync_api import sync_playwright
from langchain_core.documents import Document

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

# 1. LOAD SOURCE DATA

# -------------------------
# Text
# -------------------------
TEXT_METHOD = False

if TEXT_METHOD:
    loader = TextLoader('./src/appolo.txt')
    docs = loader.load()
    print(docs)

# -------------------------
#  Web (Playwright)
# -------------------------
WEB_METHOD = False

urls = [
    "https://medium.com/@aysebilgegunduz/everything-you-need-to-know-about-idor-insecure-direct-object-references-375f83e03a87",
    "https://medium.com/@ud4y25/idor-vulnerabilities-explained-a-researchers-guide-to-authorization-flaws-82030def0e28"
]


if WEB_METHOD:
    docs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)

            html = page.content()
            soup = bs4.BeautifulSoup(html, "html.parser")

            elements = soup.find_all(
                class_=["pw-post-title", "pw-post-body-paragraph"]
            )

            text = "\n".join(e.get_text() for e in elements)

            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": url}
                )
            )

        browser.close()

    print(docs)


# -------------------------
# PDF
# -------------------------
PDF_METHOD = True

if PDF_METHOD:
    loader = PyPDFLoader("./src/attention.pdf")
    docs = loader.load()

# 2 . LOAD SOURCE DATA | Embeddings
splitter = RecursiveCharacterTextSplitter(chunk_size = 600,chunk_overlap=150)
docs = splitter.split_documents(docs)
#print(docs[:2])

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# FAISS: fast in-memory vector store for similarity search
# Chroma: persistent vector database for storing and retrieving embeddings
# Using Chroma here for persistence and easier data management

db = Chroma(
    collection_name="rag_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

db.add_documents(docs)

query = "What is the Transformer model?"


retriever = db.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke(query)

for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---\n")
    print(doc.page_content)

# LLM Model
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

context = "\n\n".join([doc.page_content for doc in results])

prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below.

<Context>{context}</Context>

Question:
{question}
""")

document_chain = create_stuff_documents_chain(
    llm=gemini_llm,
    prompt=prompt
)
