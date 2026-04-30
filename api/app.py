from fastapi import FastAPI
import uvicorn

from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes

import settings

app = FastAPI(
    title="Langchain Server",
    version="0.1v",
    description="A simple API server"
)

add_routes(
    app,
    ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite"),
    path="/gemini"
)


gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

hf_endpoint = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
)

hf_llm = ChatHuggingFace(llm=hf_endpoint)


prompt1 = ChatPromptTemplate.from_template("Write an essay about {topic} in a maximum of 80 words.")
prompt2 = ChatPromptTemplate.from_template("Write a simple poem about {topic}.")

add_routes( app, prompt1|gemini_llm , path="/essay" )
add_routes( app, prompt2|hf_llm , path="/poem" )

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)