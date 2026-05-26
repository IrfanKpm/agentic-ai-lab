import settings
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

# ---------------- PROMPT ----------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "{question}")
    ]
)

st.title("LangChain Multi-LLM Demo")

# ---------------- INPUT ----------------
input_question = st.text_input("Ask something", key="question_input")

send_clicked = st.button("Send")

# ---------------- MODELS ----------------
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
openai_llm = ChatOpenAI(model="gpt-4o-mini")

hf_endpoint = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
)

hf_llm = ChatHuggingFace(llm=hf_endpoint)

# ---------------- MODEL ORDER ----------------
order_option = st.selectbox(
    "Select fallback order",
    [
        "hf - gemini - openai",
        "gemini - hf - openai"
    ]
)

if order_option == "hf - gemini - openai":
    primary = hf_llm
    fallbacks = [gemini_llm, openai_llm]

elif order_option == "gemini - hf - openai":
    primary = gemini_llm
    fallbacks = [hf_llm, openai_llm]

llm = primary.with_fallbacks(fallbacks)

chain = prompt | llm | StrOutputParser()

# ---------------- EXECUTION ----------------
if send_clicked and input_question:
    with st.spinner("Thinking..."):
        response = chain.invoke({"question": input_question})
        st.write(response)