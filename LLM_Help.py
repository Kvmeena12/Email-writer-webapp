from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="meta-llama/llama-4-scout-17b-16e-instruct")



if __name__ == "__main__":
    response = llm.invoke("Two most important ingradient in samosa are ")
    print(response.content)





