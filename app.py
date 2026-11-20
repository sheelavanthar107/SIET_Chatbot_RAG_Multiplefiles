import streamlit as st
from rag_engine import load_knowledge_base, ask_rag
st.set_page_config(page_title = "SIET_Chatbot", layout = "centered")
st.title("SIET-Chatbot")
st.caption("Ask Anything about College information, Courses, Placements, FAQs, Rules and Regulations")
st.caption("RAG Pipeline with Multiple files")
st.caption("Created by Harshitha")
my_key = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def initiate_rag():
  return load_knowledge_base("college_docs")

index, embed_model, chunks = initiate_rag()
if "chat_hist" not in st.session_state:   #load and display chat history if exsit if not create new
  st.session_state.chat_hist =[]

for qa in st.session_state.chat_hist :
  with st.chat_message(qa["role"]):    #acess the history from session state
    st.write(qa["content"])

question = st.chat_input("Ask anything about SIET college...")

if question:
  st.session_state.chat_hist.append(
    {"role" : "user" , "content" : question})
  with st.chat_message("user"):
    st.write(question)
  with st.chat_message("assistant"):
    with st.spinner("asking RAG for answer"):
      answer = ask_rag(question, embed_model, chunks, index, api_key = my_key)      #heart of progrM
      st.write(answer)
      st.session_state.chat_hist.append(
        {"role" : "assistant" , "content" : answer})

if st.button("Clear chat"):
  st.session_state.chat_hist = []
  st.rerun()
