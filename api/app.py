# # # # # # import streamlit as st
# # # # # # import os
# # # # # # from dotenv import load_dotenv
# # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # from langchain_chroma import Chroma
# # # # # # from langchain_groq import ChatGroq
# # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # Page Configuration
# # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # Load Environment Variables
# # # # # # load_dotenv()

# # # # # # # Sidebar for Status
# # # # # # with st.sidebar:
# # # # # #     st.header("System Status")
# # # # # #     if os.path.exists("./db"):
# # # # # #         st.success("Database: Connected")
# # # # # #     else:
# # # # # #         st.error("Database: Not Found! Run ingest.py first.")
    
# # # # # #     if st.button("Clear Chat History"):
# # # # # #         st.session_state.messages = []

# # # # # # # Initialize Models (Cached for speed)
# # # # # # @st.cache_resource
# # # # # # def load_rag_system():
# # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # #     vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # #     llm = ChatGroq(
# # # # # #         groq_api_key=os.getenv("GROQ_API_KEY"),
# # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # #         temperature=0.2
# # # # # #     )
# # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # #     Context: {context}
# # # # # #     Question: {input}
# # # # # #     Answer:""")
    
# # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # chain = load_rag_system()

# # # # # # # Chat History Setup
# # # # # # if "messages" not in st.session_state:
# # # # # #     st.session_state.messages = []

# # # # # # # Display chat messages from history
# # # # # # for message in st.session_state.messages:
# # # # # #     with st.chat_message(message["role"]):
# # # # # #         st.markdown(message["content"])

# # # # # # # User Input
# # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # #     # Add user message to history
# # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # #     with st.chat_message("user"):
# # # # # #         st.markdown(prompt)

# # # # # #     # Generate Response
# # # # # #     with st.chat_message("assistant"):
# # # # # #         with st.spinner("Thinking..."):
# # # # # #             response = chain.invoke({"input": prompt})
# # # # # #             full_response = response["answer"]
# # # # # #             st.markdown(full_response)
    
# # # # # #     # Add assistant response to history
# # # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})





# # # # # # -------------------------------------------------------------------------
# # # # # # CRITICAL FIX: This must be the very first code in the file
# # # # # # This swaps the system sqlite3 with pysqlite3-binary for ChromaDB support
# # # # # # __import__('pysqlite3')
# # # # # # import sys
# # # # # # sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # -------------------------------------------------------------------------

# # # # # import streamlit as st
# # # # # import os
# # # # # from dotenv import load_dotenv
# # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # from langchain_chroma import Chroma
# # # # # from langchain_groq import ChatGroq
# # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # from langchain.chains import create_retrieval_chain

# # # # # # Page Configuration
# # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # Load Environment Variables (Try .env first, fallback to st.secrets)
# # # # # load_dotenv()

# # # # # # Securely get API Key
# # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # if not groq_api_key and "GROQ_API_KEY" in st.secrets:
# # # # #     groq_api_key = st.secrets["GROQ_API_KEY"]

# # # # # if not groq_api_key:
# # # # #     st.error("⚠️ GROQ_API_KEY is missing! Please add it to .env or Streamlit Secrets.")
# # # # #     st.stop()

# # # # # # Sidebar for Status
# # # # # db_path = "./db"
# # # # # db_exists = os.path.exists(db_path) and os.listdir(db_path)

# # # # # with st.sidebar:
# # # # #     st.header("System Status")
# # # # #     if db_exists:
# # # # #         st.success("Database: Connected")
# # # # #     else:
# # # # #         st.error("Database: Not Found!")
# # # # #         st.warning("⚠️ Please run `ingest.py` locally and commit the `db` folder to GitHub.")
    
# # # # #     if st.button("Clear Chat History"):
# # # # #         st.session_state.messages = []
# # # # #         st.rerun()

# # # # # # Initialize Models (Cached for speed)
# # # # # @st.cache_resource
# # # # # def load_rag_system():
# # # # #     # Only load if DB exists to avoid crashing
# # # # #     if not os.path.exists(db_path):
# # # # #         return None

# # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
# # # # #     # Initialize Chroma
# # # # #     vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
# # # # #     llm = ChatGroq(
# # # # #         groq_api_key=groq_api_key,
# # # # #         model_name="llama-3.3-70b-versatile",
# # # # #         temperature=0.2
# # # # #     )
    
# # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # #     Use the following pieces of retrieved context to answer the question. 
# # # # #     If you don't know the answer, just say that you don't know. 
    
# # # # #     Context: {context}
    
# # # # #     Question: {input}
# # # # #     Answer:""")
    
# # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # Load the chain
# # # # # if db_exists:
# # # # #     try:
# # # # #         chain = load_rag_system()
# # # # #     except Exception as e:
# # # # #         st.error(f"Error loading model: {e}")
# # # # #         chain = None
# # # # # else:
# # # # #     chain = None

# # # # # # Chat History Setup
# # # # # if "messages" not in st.session_state:
# # # # #     st.session_state.messages = []

# # # # # # Display chat messages from history
# # # # # for message in st.session_state.messages:
# # # # #     with st.chat_message(message["role"]):
# # # # #         st.markdown(message["content"])

# # # # # # User Input
# # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # #     # Add user message to history
# # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # #     with st.chat_message("user"):
# # # # #         st.markdown(prompt)

# # # # #     # Check if system is ready
# # # # #     if not chain:
# # # # #         st.error("The AI Brain is not loaded. Please ensure the database is generated and uploaded.")
# # # # #     else:
# # # # #         # Generate Response
# # # # #         with st.chat_message("assistant"):
# # # # #             with st.spinner("Searching knowledge base..."):
# # # # #                 try:
# # # # #                     response = chain.invoke({"input": prompt})
# # # # #                     full_response = response["answer"]
# # # # #                     st.markdown(full_response)
                    
# # # # #                     # Add assistant response to history
# # # # #                     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # #                 except Exception as e:
# # # # #                     st.error(f"An error occurred: {str(e)}")



# # # # # node js conversion



# # # # from fastapi import FastAPI, Request
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # import os
# # # # from dotenv import load_dotenv
# # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # from langchain_chroma import Chroma
# # # # from langchain_groq import ChatGroq
# # # # from langchain_core.prompts import ChatPromptTemplate
# # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # from langchain.chains import create_retrieval_chain

# # # # load_dotenv()
# # # # app = FastAPI()

# # # # # CORS allow karein taake frontend connect ho sake
# # # # app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# # # # # Load RAG System
# # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile", temperature=0.2)

# # # # prompt = ChatPromptTemplate.from_template("""
# # # # You are a professional customer support assistant for ZT Hosting. 
# # # # Context: {context}
# # # # Question: {input}
# # # # Answer:""")

# # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # @app.post("/ask")
# # # # async def ask_bot(request: Request):
# # # #     data = await request.json()
# # # #     user_input = data.get("message")
# # # #     response = chain.invoke({"input": user_input})
# # # #     return {"answer": response["answer"]}



# # # # update the path of the db becuase we have move the app.py into the api folder


# # # from fastapi import FastAPI, Request
# # # from fastapi.middleware.cors import CORSMiddleware
# # # import os
# # # from dotenv import load_dotenv
# # # from langchain_huggingface import HuggingFaceEmbeddings
# # # from langchain_chroma import Chroma
# # # from langchain_groq import ChatGroq
# # # from langchain_core.prompts import ChatPromptTemplate
# # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # from langchain.chains import create_retrieval_chain

# # # # Environment variables load karein
# # # load_dotenv()

# # # app = FastAPI()

# # # # CORS settings: Taake aapka frontend backend se asani se baat kar sake
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # --- Path Correction ---
# # # # Chunkay ye file 'api' folder mein hai, humein '../db' use karna hoga 
# # # # taake code ek step piche ja kar 'db' folder ko dhund sakay.
# # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # Load RAG System
# # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # Vector Database check aur connection
# # # if os.path.exists(DB_PATH):
# # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # else:
# # #     print(f"Warning: Database folder not found at {DB_PATH}")
# # #     vector_db = None

# # # llm = ChatGroq(
# # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # #     model_name="llama-3.3-70b-versatile", 
# # #     temperature=0.2
# # # )

# # # prompt = ChatPromptTemplate.from_template("""
# # # You are a professional customer support assistant for ZT Hosting. 
# # # Use the provided context to answer the user's question accurately.
# # # If you don't know the answer, politely say so.

# # # Context: {context}
# # # Question: {input}
# # # Answer:""")

# # # # Chain Setup
# # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # if vector_db:
# # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # else:
# # #     chain = None

# # # @app.post("/ask")
# # # async def ask_bot(request: Request):
# # #     if not chain:
# # #         return {"answer": "Error: AI database not found. Please check paths."}
        
# # #     data = await request.json()
# # #     user_input = data.get("message")
    
# # #     try:
# # #         response = chain.invoke({"input": user_input})
# # #         return {"answer": response["answer"]}
# # #     except Exception as e:
# # #         return {"answer": f"Sorry, an error occurred: {str(e)}"}




# # # update the code to fix the crash isssue of chatbot


# # # --- SQLite Fix (Deployment ke liye zaroori) ---
# # try:
# #     __import__('pysqlite3')
# #     import sys
# #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # except ImportError:
# #     pass 

# # import os
# # from fastapi import FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from dotenv import load_dotenv
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_chroma import Chroma
# # from langchain_groq import ChatGroq
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain.chains.combine_documents import create_stuff_documents_chain
# # from langchain.chains import create_retrieval_chain

# # load_dotenv()
# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # --- Path Handling ---
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # DB_PATH = os.path.join(BASE_DIR, "db")

# # # Load Models
# # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # Database Connect
# # if os.path.exists(DB_PATH):
# #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # else:
# #     vector_db = None

# # llm = ChatGroq(
# #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# #     model_name="llama-3.3-70b-versatile", 
# #     temperature=0.2
# # )

# # prompt = ChatPromptTemplate.from_template("""
# # You are a professional customer support assistant for ZT Hosting. 
# # Context: {context}
# # Question: {input}
# # Answer:""")

# # document_chain = create_stuff_documents_chain(llm, prompt)

# # if vector_db:
# #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # else:
# #     chain = None

# # @app.post("/ask")
# # async def ask_bot(request: Request):
# #     if not chain:
# #         return {"answer": "Error: Database folder not found. Please ensure 'db' folder is uploaded."}
    
# #     data = await request.json()
# #     user_input = data.get("message")
    
# #     try:
# #         response = chain.invoke({"input": user_input})
# #         return {"answer": response["answer"]}
# #     except Exception as e:
# #         return {"answer": f"AI Error: {str(e)}"}


# # Vercel par 250 MB ki limit exceed hone ki sab se bari wajah langchain-huggingface library hai, kyunke ye apne saath PyTorch aur heavy models download karti hai. Isay bypass karne ke liye humein "Lightweight" approach apnaani hogi.

# # Niche diya gaya code aapke api/app.py ko optimize kar dega taake size kam ho jaye:




# try:
#     __import__('pysqlite3')
#     import sys
#     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# except ImportError:
#     pass 

# import os
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# # Lightweight Embeddings and Components
# from langchain_community.embeddings import HealthcareHuggingFaceEmbeddings # Ya niche wala alternative
# from langchain_community.embeddings import HuggingFaceEmbeddings 
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain

# load_dotenv()
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Path Handling ---
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "db")

# # Load Models - optimized for size
# # Note: all-MiniLM-L6-v2 is small, but the library matters
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # Database Connect
# if os.path.exists(DB_PATH):
#     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# else:
#     vector_db = None

# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="llama-3.3-70b-versatile", 
#     temperature=0.2
# )

# prompt = ChatPromptTemplate.from_template("""
# You are a professional customer support assistant for ZT Hosting. 
# Context: {context}
# Question: {input}
# Answer:""")

# document_chain = create_stuff_documents_chain(llm, prompt)

# if vector_db:
#     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# else:
#     chain = None

# @app.post("/ask")
# async def ask_bot(request: Request):
#     if not chain:
#         return {"answer": "Error: Database folder not found."}
    
#     data = await request.json()
#     user_input = data.get("message")
    
#     try:
#         response = chain.invoke({"input": user_input})
#         return {"answer": response["answer"]}
#     except Exception as e:
#         return {"answer": f"AI Error: {str(e)}"}



# try:
#     __import__('pysqlite3')
#     import sys
#     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# except ImportError:
#     pass 

# import os
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain

# load_dotenv()
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "db")

# # Memory-efficient embeddings
# embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# if os.path.exists(DB_PATH):
#     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# else:
#     vector_db = None

# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="llama-3.3-70b-versatile", 
#     temperature=0.2
# )

# prompt = ChatPromptTemplate.from_template("""
# You are a professional customer support assistant for ZT Hosting. 
# Context: {context}
# Question: {input}
# Answer:""")

# document_chain = create_stuff_documents_chain(llm, prompt)
# chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# @app.post("/ask")
# async def ask_bot(request: Request):
#     if not chain:
#         return {"answer": "Error: Database folder not found."}
#     data = await request.json()
#     user_input = data.get("message")
#     try:
#         response = chain.invoke({"input": user_input})
#         return {"answer": response["answer"]}
#     except Exception as e:
#         return {"answer": f"AI Error: {str(e)}"}



try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass 

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path Handling
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db")

# Wahi embeddings jo database banate waqt use kiye
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

if os.path.exists(DB_PATH):
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
else:
    vector_db = None

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.3-70b-versatile", 
    temperature=0.2
)

prompt = ChatPromptTemplate.from_template("""
You are a professional customer support assistant for ZT Hosting. 
Context: {context}
Question: {input}
Answer:""")

document_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

@app.post("/ask")
async def ask_bot(request: Request):
    if not chain:
        return {"answer": "Error: Database folder not found."}
    data = await request.json()
    user_input = data.get("message")
    try:
        response = chain.invoke({"input": user_input})
        return {"answer": response["answer"]}
    except Exception as e:
        return {"answer": f"AI Error: {str(e)}"}
    
    