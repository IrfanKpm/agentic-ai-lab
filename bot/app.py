import settings
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "{question}")
    ]
)

st.title("LangChain Multi-LLM Demo")
input_question = st.text_input("Ask something")

# Primary model
gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")


# Backup model (Gemini)
openai_llm = ChatOpenAI(model="gpt-4o-mini")

# fallback setup
llm = gemini_llm.with_fallbacks([gemini_llm])

chain = prompt | llm | StrOutputParser()

if input_question:
    response = chain.invoke({"question": input_question})
    st.write(response)