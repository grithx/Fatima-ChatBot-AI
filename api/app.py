# # # # # # # # # # # import streamlit as st
# # # # # # # # # # # import os
# # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # Page Configuration
# # # # # # # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # # # # # # Load Environment Variables
# # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # Sidebar for Status
# # # # # # # # # # # with st.sidebar:
# # # # # # # # # # #     st.header("System Status")
# # # # # # # # # # #     if os.path.exists("./db"):
# # # # # # # # # # #         st.success("Database: Connected")
# # # # # # # # # # #     else:
# # # # # # # # # # #         st.error("Database: Not Found! Run ingest.py first.")
    
# # # # # # # # # # #     if st.button("Clear Chat History"):
# # # # # # # # # # #         st.session_state.messages = []

# # # # # # # # # # # # Initialize Models (Cached for speed)
# # # # # # # # # # # @st.cache_resource
# # # # # # # # # # # def load_rag_system():
# # # # # # # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # # # # # # #     vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # # # # # # #     llm = ChatGroq(
# # # # # # # # # # #         groq_api_key=os.getenv("GROQ_API_KEY"),
# # # # # # # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # # # # # # #         temperature=0.2
# # # # # # # # # # #     )
# # # # # # # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # #     Context: {context}
# # # # # # # # # # #     Question: {input}
# # # # # # # # # # #     Answer:""")
    
# # # # # # # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # chain = load_rag_system()

# # # # # # # # # # # # Chat History Setup
# # # # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # # # #     st.session_state.messages = []

# # # # # # # # # # # # Display chat messages from history
# # # # # # # # # # # for message in st.session_state.messages:
# # # # # # # # # # #     with st.chat_message(message["role"]):
# # # # # # # # # # #         st.markdown(message["content"])

# # # # # # # # # # # # User Input
# # # # # # # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # # # # # # #     # Add user message to history
# # # # # # # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # # # # # #     with st.chat_message("user"):
# # # # # # # # # # #         st.markdown(prompt)

# # # # # # # # # # #     # Generate Response
# # # # # # # # # # #     with st.chat_message("assistant"):
# # # # # # # # # # #         with st.spinner("Thinking..."):
# # # # # # # # # # #             response = chain.invoke({"input": prompt})
# # # # # # # # # # #             full_response = response["answer"]
# # # # # # # # # # #             st.markdown(full_response)
    
# # # # # # # # # # #     # Add assistant response to history
# # # # # # # # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})





# # # # # # # # # # # -------------------------------------------------------------------------
# # # # # # # # # # # CRITICAL FIX: This must be the very first code in the file
# # # # # # # # # # # This swaps the system sqlite3 with pysqlite3-binary for ChromaDB support
# # # # # # # # # # # __import__('pysqlite3')
# # # # # # # # # # # import sys
# # # # # # # # # # # sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # -------------------------------------------------------------------------

# # # # # # # # # # import streamlit as st
# # # # # # # # # # import os
# # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # Page Configuration
# # # # # # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # # # # # Load Environment Variables (Try .env first, fallback to st.secrets)
# # # # # # # # # # load_dotenv()

# # # # # # # # # # # Securely get API Key
# # # # # # # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # # # # # # if not groq_api_key and "GROQ_API_KEY" in st.secrets:
# # # # # # # # # #     groq_api_key = st.secrets["GROQ_API_KEY"]

# # # # # # # # # # if not groq_api_key:
# # # # # # # # # #     st.error("⚠️ GROQ_API_KEY is missing! Please add it to .env or Streamlit Secrets.")
# # # # # # # # # #     st.stop()

# # # # # # # # # # # Sidebar for Status
# # # # # # # # # # db_path = "./db"
# # # # # # # # # # db_exists = os.path.exists(db_path) and os.listdir(db_path)

# # # # # # # # # # with st.sidebar:
# # # # # # # # # #     st.header("System Status")
# # # # # # # # # #     if db_exists:
# # # # # # # # # #         st.success("Database: Connected")
# # # # # # # # # #     else:
# # # # # # # # # #         st.error("Database: Not Found!")
# # # # # # # # # #         st.warning("⚠️ Please run `ingest.py` locally and commit the `db` folder to GitHub.")
    
# # # # # # # # # #     if st.button("Clear Chat History"):
# # # # # # # # # #         st.session_state.messages = []
# # # # # # # # # #         st.rerun()

# # # # # # # # # # # Initialize Models (Cached for speed)
# # # # # # # # # # @st.cache_resource
# # # # # # # # # # def load_rag_system():
# # # # # # # # # #     # Only load if DB exists to avoid crashing
# # # # # # # # # #     if not os.path.exists(db_path):
# # # # # # # # # #         return None

# # # # # # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
# # # # # # # # # #     # Initialize Chroma
# # # # # # # # # #     vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
# # # # # # # # # #     llm = ChatGroq(
# # # # # # # # # #         groq_api_key=groq_api_key,
# # # # # # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # # # # # #         temperature=0.2
# # # # # # # # # #     )
    
# # # # # # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # #     Use the following pieces of retrieved context to answer the question. 
# # # # # # # # # #     If you don't know the answer, just say that you don't know. 
    
# # # # # # # # # #     Context: {context}
    
# # # # # # # # # #     Question: {input}
# # # # # # # # # #     Answer:""")
    
# # # # # # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # Load the chain
# # # # # # # # # # if db_exists:
# # # # # # # # # #     try:
# # # # # # # # # #         chain = load_rag_system()
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         st.error(f"Error loading model: {e}")
# # # # # # # # # #         chain = None
# # # # # # # # # # else:
# # # # # # # # # #     chain = None

# # # # # # # # # # # Chat History Setup
# # # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # # #     st.session_state.messages = []

# # # # # # # # # # # Display chat messages from history
# # # # # # # # # # for message in st.session_state.messages:
# # # # # # # # # #     with st.chat_message(message["role"]):
# # # # # # # # # #         st.markdown(message["content"])

# # # # # # # # # # # User Input
# # # # # # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # # # # # #     # Add user message to history
# # # # # # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # # # # #     with st.chat_message("user"):
# # # # # # # # # #         st.markdown(prompt)

# # # # # # # # # #     # Check if system is ready
# # # # # # # # # #     if not chain:
# # # # # # # # # #         st.error("The AI Brain is not loaded. Please ensure the database is generated and uploaded.")
# # # # # # # # # #     else:
# # # # # # # # # #         # Generate Response
# # # # # # # # # #         with st.chat_message("assistant"):
# # # # # # # # # #             with st.spinner("Searching knowledge base..."):
# # # # # # # # # #                 try:
# # # # # # # # # #                     response = chain.invoke({"input": prompt})
# # # # # # # # # #                     full_response = response["answer"]
# # # # # # # # # #                     st.markdown(full_response)
                    
# # # # # # # # # #                     # Add assistant response to history
# # # # # # # # # #                     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # # # # # # #                 except Exception as e:
# # # # # # # # # #                     st.error(f"An error occurred: {str(e)}")



# # # # # # # # # # node js conversion



# # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # import os
# # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # load_dotenv()
# # # # # # # # # app = FastAPI()

# # # # # # # # # # CORS allow karein taake frontend connect ho sake
# # # # # # # # # app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# # # # # # # # # # Load RAG System
# # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # # # # # vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # # # # # llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile", temperature=0.2)

# # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # Context: {context}
# # # # # # # # # Question: {input}
# # # # # # # # # Answer:""")

# # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # @app.post("/ask")
# # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # #     data = await request.json()
# # # # # # # # #     user_input = data.get("message")
# # # # # # # # #     response = chain.invoke({"input": user_input})
# # # # # # # # #     return {"answer": response["answer"]}



# # # # # # # # # update the path of the db becuase we have move the app.py into the api folder


# # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # import os
# # # # # # # # from dotenv import load_dotenv
# # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # from langchain_chroma import Chroma
# # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # Environment variables load karein
# # # # # # # # load_dotenv()

# # # # # # # # app = FastAPI()

# # # # # # # # # CORS settings: Taake aapka frontend backend se asani se baat kar sake
# # # # # # # # app.add_middleware(
# # # # # # # #     CORSMiddleware,
# # # # # # # #     allow_origins=["*"],
# # # # # # # #     allow_credentials=True,
# # # # # # # #     allow_methods=["*"],
# # # # # # # #     allow_headers=["*"],
# # # # # # # # )

# # # # # # # # # --- Path Correction ---
# # # # # # # # # Chunkay ye file 'api' folder mein hai, humein '../db' use karna hoga 
# # # # # # # # # taake code ek step piche ja kar 'db' folder ko dhund sakay.
# # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # Load RAG System
# # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # Vector Database check aur connection
# # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # else:
# # # # # # # #     print(f"Warning: Database folder not found at {DB_PATH}")
# # # # # # # #     vector_db = None

# # # # # # # # llm = ChatGroq(
# # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # #     temperature=0.2
# # # # # # # # )

# # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # Use the provided context to answer the user's question accurately.
# # # # # # # # If you don't know the answer, politely say so.

# # # # # # # # Context: {context}
# # # # # # # # Question: {input}
# # # # # # # # Answer:""")

# # # # # # # # # Chain Setup
# # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # if vector_db:
# # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # else:
# # # # # # # #     chain = None

# # # # # # # # @app.post("/ask")
# # # # # # # # async def ask_bot(request: Request):
# # # # # # # #     if not chain:
# # # # # # # #         return {"answer": "Error: AI database not found. Please check paths."}
        
# # # # # # # #     data = await request.json()
# # # # # # # #     user_input = data.get("message")
    
# # # # # # # #     try:
# # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # #         return {"answer": response["answer"]}
# # # # # # # #     except Exception as e:
# # # # # # # #         return {"answer": f"Sorry, an error occurred: {str(e)}"}




# # # # # # # # update the code to fix the crash isssue of chatbot


# # # # # # # # --- SQLite Fix (Deployment ke liye zaroori) ---
# # # # # # # try:
# # # # # # #     __import__('pysqlite3')
# # # # # # #     import sys
# # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # except ImportError:
# # # # # # #     pass 

# # # # # # # import os
# # # # # # # from fastapi import FastAPI, Request
# # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # from dotenv import load_dotenv
# # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # from langchain_chroma import Chroma
# # # # # # # from langchain_groq import ChatGroq
# # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # load_dotenv()
# # # # # # # app = FastAPI()

# # # # # # # app.add_middleware(
# # # # # # #     CORSMiddleware,
# # # # # # #     allow_origins=["*"],
# # # # # # #     allow_credentials=True,
# # # # # # #     allow_methods=["*"],
# # # # # # #     allow_headers=["*"],
# # # # # # # )

# # # # # # # # --- Path Handling ---
# # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # Load Models
# # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # Database Connect
# # # # # # # if os.path.exists(DB_PATH):
# # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # else:
# # # # # # #     vector_db = None

# # # # # # # llm = ChatGroq(
# # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # #     temperature=0.2
# # # # # # # )

# # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # Context: {context}
# # # # # # # Question: {input}
# # # # # # # Answer:""")

# # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # if vector_db:
# # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # else:
# # # # # # #     chain = None

# # # # # # # @app.post("/ask")
# # # # # # # async def ask_bot(request: Request):
# # # # # # #     if not chain:
# # # # # # #         return {"answer": "Error: Database folder not found. Please ensure 'db' folder is uploaded."}
    
# # # # # # #     data = await request.json()
# # # # # # #     user_input = data.get("message")
    
# # # # # # #     try:
# # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # #         return {"answer": response["answer"]}
# # # # # # #     except Exception as e:
# # # # # # #         return {"answer": f"AI Error: {str(e)}"}


# # # # # # # Vercel par 250 MB ki limit exceed hone ki sab se bari wajah langchain-huggingface library hai, kyunke ye apne saath PyTorch aur heavy models download karti hai. Isay bypass karne ke liye humein "Lightweight" approach apnaani hogi.

# # # # # # # Niche diya gaya code aapke api/app.py ko optimize kar dega taake size kam ho jaye:




# # # # # # try:
# # # # # #     __import__('pysqlite3')
# # # # # #     import sys
# # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # except ImportError:
# # # # # #     pass 

# # # # # # import os
# # # # # # from fastapi import FastAPI, Request
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from dotenv import load_dotenv

# # # # # # # Lightweight Embeddings and Components
# # # # # # from langchain_community.embeddings import HealthcareHuggingFaceEmbeddings # Ya niche wala alternative
# # # # # # from langchain_community.embeddings import HuggingFaceEmbeddings 
# # # # # # from langchain_chroma import Chroma
# # # # # # from langchain_groq import ChatGroq
# # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # from langchain.chains import create_retrieval_chain

# # # # # # load_dotenv()
# # # # # # app = FastAPI()

# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=["*"],
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )

# # # # # # # --- Path Handling ---
# # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # Load Models - optimized for size
# # # # # # # Note: all-MiniLM-L6-v2 is small, but the library matters
# # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # Database Connect
# # # # # # if os.path.exists(DB_PATH):
# # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # else:
# # # # # #     vector_db = None

# # # # # # llm = ChatGroq(
# # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # #     temperature=0.2
# # # # # # )

# # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # Context: {context}
# # # # # # Question: {input}
# # # # # # Answer:""")

# # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # if vector_db:
# # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # else:
# # # # # #     chain = None

# # # # # # @app.post("/ask")
# # # # # # async def ask_bot(request: Request):
# # # # # #     if not chain:
# # # # # #         return {"answer": "Error: Database folder not found."}
    
# # # # # #     data = await request.json()
# # # # # #     user_input = data.get("message")
    
# # # # # #     try:
# # # # # #         response = chain.invoke({"input": user_input})
# # # # # #         return {"answer": response["answer"]}
# # # # # #     except Exception as e:
# # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # try:
# # # # # #     __import__('pysqlite3')
# # # # # #     import sys
# # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # except ImportError:
# # # # # #     pass 

# # # # # # import os
# # # # # # from fastapi import FastAPI, Request
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from dotenv import load_dotenv
# # # # # # from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# # # # # # from langchain_chroma import Chroma
# # # # # # from langchain_groq import ChatGroq
# # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # from langchain.chains import create_retrieval_chain

# # # # # # load_dotenv()
# # # # # # app = FastAPI()

# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=["*"],
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )

# # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # Memory-efficient embeddings
# # # # # # embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# # # # # # if os.path.exists(DB_PATH):
# # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # else:
# # # # # #     vector_db = None

# # # # # # llm = ChatGroq(
# # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # #     temperature=0.2
# # # # # # )

# # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # Context: {context}
# # # # # # Question: {input}
# # # # # # Answer:""")

# # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# # # # # # @app.post("/ask")
# # # # # # async def ask_bot(request: Request):
# # # # # #     if not chain:
# # # # # #         return {"answer": "Error: Database folder not found."}
# # # # # #     data = await request.json()
# # # # # #     user_input = data.get("message")
# # # # # #     try:
# # # # # #         response = chain.invoke({"input": user_input})
# # # # # #         return {"answer": response["answer"]}
# # # # # #     except Exception as e:
# # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # try:
# # # # #     __import__('pysqlite3')
# # # # #     import sys
# # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # except ImportError:
# # # # #     pass 

# # # # # import os
# # # # # from fastapi import FastAPI, Request
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from dotenv import load_dotenv
# # # # # from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# # # # # from langchain_chroma import Chroma
# # # # # from langchain_groq import ChatGroq
# # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # from langchain.chains import create_retrieval_chain

# # # # # load_dotenv()
# # # # # app = FastAPI()

# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # # Path Handling
# # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # Wahi embeddings jo database banate waqt use kiye
# # # # # embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# # # # # if os.path.exists(DB_PATH):
# # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # else:
# # # # #     vector_db = None

# # # # # llm = ChatGroq(
# # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # #     model_name="llama-3.3-70b-versatile", 
# # # # #     temperature=0.2
# # # # # )

# # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # Context: {context}
# # # # # Question: {input}
# # # # # Answer:""")

# # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# # # # # @app.post("/ask")
# # # # # async def ask_bot(request: Request):
# # # # #     if not chain:
# # # # #         return {"answer": "Error: Database folder not found."}
# # # # #     data = await request.json()
# # # # #     user_input = data.get("message")
# # # # #     try:
# # # # #         response = chain.invoke({"input": user_input})
# # # # #         return {"answer": response["answer"]}
# # # # #     except Exception as e:
# # # # #         return {"answer": f"AI Error: {str(e)}"}
    


# # # # # ye code bina kisi local embedding model ke chahay ga. Ye seedha text file (zt_data.txt) ko read karega aur Groq ko bhej dega. Ye 100% 250MB se kam hoga.


# # # # import os
# # # # from fastapi import FastAPI, Request
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from dotenv import load_dotenv
# # # # from langchain_groq import ChatGroq
# # # # from langchain_core.prompts import ChatPromptTemplate

# # # # load_dotenv()
# # # # app = FastAPI()

# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=["*"],
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )

# # # # # Knowledge Base Read Karein
# # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")

# # # # def get_context():
# # # #     if os.path.exists(DATA_PATH):
# # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # #             return f.read()[:10000] # Pehle 10k characters (Vercel limits ke liye)
# # # #     return "No hosting info available."

# # # # llm = ChatGroq(
# # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # #     model_name="llama-3.3-70b-versatile", 
# # # #     temperature=0.2
# # # # )

# # # # prompt = ChatPromptTemplate.from_template("""
# # # # You are a professional customer support assistant for ZT Hosting. 
# # # # Use the following context to answer:
# # # # {context}

# # # # User Question: {input}
# # # # Answer:""")

# # # # @app.post("/ask")
# # # # async def ask_bot(request: Request):
# # # #     data = await request.json()
# # # #     user_input = data.get("message")
# # # #     context = get_context()
    
# # # #     try:
# # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # #         response = llm.invoke(full_prompt)
# # # #         return {"answer": response.content}
# # # #     except Exception as e:
# # # #         return {"answer": f"AI Error: {str(e)}"}



# # # import os
# # # from fastapi import FastAPI, Request
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.responses import HTMLResponse # Naya import
# # # from dotenv import load_dotenv
# # # from langchain_groq import ChatGroq
# # # from langchain_core.prompts import ChatPromptTemplate

# # # load_dotenv()
# # # app = FastAPI()

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html") # HTML ka path

# # # # --- Naya Route: Chatbot ka Page dikhane ke liye ---
# # # @app.get("/", response_class=HTMLResponse)
# # # async def get_index():
# # #     if os.path.exists(HTML_PATH):
# # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # #             return f.read()
# # #     return "<h1>Index.html not found in templates/</h1>"

# # # def get_context():
# # #     if os.path.exists(DATA_PATH):
# # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # #             return f.read()[:10000]
# # #     return "No hosting info available."

# # # llm = ChatGroq(
# # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # #     model_name="llama-3.3-70b-versatile", 
# # #     temperature=0.2
# # # )

# # # prompt = ChatPromptTemplate.from_template("""
# # # You are a professional customer support assistant for ZT Hosting. 
# # # Use the following context to answer:
# # # {context}

# # # User Question: {input}
# # # Answer:""")

# # # @app.post("/ask")
# # # async def ask_bot(request: Request):
# # #     data = await request.json()
# # #     user_input = data.get("message")
# # #     context = get_context()
# # #     try:
# # #         full_prompt = prompt.format(context=context, input=user_input)
# # #         response = llm.invoke(full_prompt)
# # #         return {"answer": response.content}
# # #     except Exception as e:
# # #         return {"answer": f"AI Error: {str(e)}"}



# # import os
# # from fastapi import FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse
# # from dotenv import load_dotenv
# # from langchain_groq import ChatGroq
# # from langchain_core.prompts import ChatPromptTemplate

# # load_dotenv()
# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Path settings
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # Aapki index.html ka sahi path
# # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# # # 🏠 Home Route: Ye aapka interface dikhayega
# # @app.get("/", response_class=HTMLResponse)
# # async def get_home():
# #     try:
# #         if os.path.exists(HTML_PATH):
# #             with open(HTML_PATH, "r", encoding="utf-8") as f:
# #                 return f.read()
# #         return "<h1>Error: templates/index.html not found!</h1>"
# #     except Exception as e:
# #         return f"<h1>Internal Error: {str(e)}</h1>"

# # # 🤖 AI Logic
# # def get_context():
# #     if os.path.exists(DATA_PATH):
# #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# #             return f.read()[:10000]
# #     return "No hosting info available."

# # llm = ChatGroq(
# #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# #     model_name="llama-3.3-70b-versatile", 
# #     temperature=0.2
# # )

# # prompt = ChatPromptTemplate.from_template("""
# # You are a professional customer support assistant for ZT Hosting. 
# # Use the following context to answer the user:
# # {context}

# # User Question: {input}
# # Answer:""")

# # # 💬 API Route: Ye chat ka jawab dega
# # @app.post("/ask")
# # async def ask_bot(request: Request):
# #     data = await request.json()
# #     user_input = data.get("message")
# #     context = get_context()
# #     try:
# #         full_prompt = prompt.format(context=context, input=user_input)
# #         response = llm.invoke(full_prompt)
# #         return {"answer": response.content}
# #     except Exception as e:
# #         return {"answer": f"AI Error: {str(e)}"}


# # update code to give the Bilkul, ye raha aapka complete updated api/app.py. Maine is mein aapka naya professional prompt, temperature settings, aur file paths ko organize kar diya hai taake bot bilkul to-the-point jawab de.



# import os
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate

# load_dotenv()
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Path Settings ---
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# # --- UI Route ---
# @app.get("/", response_class=HTMLResponse)
# async def get_home():
#     try:
#         if os.path.exists(HTML_PATH):
#             with open(HTML_PATH, "r", encoding="utf-8") as f:
#                 return f.read()
#         return "<h1>Error: templates/index.html not found!</h1>"
#     except Exception as e:
#         return f"<h1>Internal Error: {str(e)}</h1>"

# # --- AI Logic & Professional Prompting ---
# def get_context():
#     if os.path.exists(DATA_PATH):
#         with open(DATA_PATH, "r", encoding="utf-8") as f:
#             # Context window limit to avoid token overflow
#             return f.read()[:8000]
#     return "No hosting info available."

# # Low temperature (0.1) keeps the bot factual and avoids 'hallucinations'
# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="llama-3.3-70b-versatile", 
#     temperature=0.1 
# )

# # Professional & Structured Prompt
# prompt = ChatPromptTemplate.from_template("""
# You are the Official ZT Hosting Support AI. Your goal is to provide concise, professional, and structured information.

# STRICT GUIDELINES:
# 1. ONLY use information from the provided context. If not found, say you don't know politely.
# 2. BE CONCISE: Answer directly. No "Hello", "I hope you're well", or long intros. 
# 3. FORMATTING: Use **bold** for prices and plan names. Use bullet points for features.
# 4. STRUCTURE: Responses must be highly organized. Use tables for plan comparisons.
# 5. NO EXTRA INFO: Do not suggest other plans unless requested.
# 6. LANGUAGE: If the question is in Roman Urdu, respond in Roman Urdu with this same professional structure.

# Context:
# {context}

# User Question: {input}
# Answer:""")

# # --- Chat API Route ---
# @app.post("/ask")
# async def ask_bot(request: Request):
#     try:
#         data = await request.json()
#         user_input = data.get("message")
        
#         if not user_input:
#             return {"answer": "Please provide a message."}

#         context = get_context()
        
#         # Generating structured response
#         full_prompt = prompt.format(context=context, input=user_input)
#         response = llm.invoke(full_prompt)
        
#         return {"answer": response.content}
    
#     except Exception as e:
#         return {"answer": f"System Error: {str(e)}"}



# Aapki app.py FastAPI use kar rahi hai, jo ke bohat achi baat hai kyunki ye Flask se fast hai. Ab hum isi file mein Admin Side logic aur Supabase Vector Search ko integrate karenge.



import os
import requests
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from supabase import create_client

load_dotenv()
app = FastAPI()
security = HTTPBasic()

# --- Security: Admin Authentication ---
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "eagale123" # Sir ke liye password
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return credentials.username

# --- Middleware & Database ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Path Settings ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# --- Helpers: Vector Generation ---
def get_embedding(text):
    # HuggingFace API use kar ke text ko numbers (vectors) mein badalna
    api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    response = requests.post(api_url, headers=headers, json={"inputs": text})
    return response.json()

# --- UI Routes ---
@app.get("/", response_class=HTMLResponse)
async def get_home():
    if os.path.exists(HTML_PATH):
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: templates/index.html not found!</h1>"

@app.get("/eagale-admin-secret", response_class=HTMLResponse)
async def get_admin(username: str = Depends(authenticate)):
    if os.path.exists(ADMIN_HTML_PATH):
        with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: templates/admin.html not found!</h1>"

# --- Admin API: Data Save to DB ---
@app.post("/admin/add-to-db")
async def save_to_db(request: Request, username: str = Depends(authenticate)):
    data = await request.json()
    q, a = data.get("question"), data.get("answer")
    vector = get_embedding(q)
    
    supabase.table("bot_knowledge").insert({
        "question": q, 
        "answer": a, 
        "embedding": vector
    }).execute()
    
    return {"message": "Success! Database updated."}

# --- AI Logic & Chat API ---
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.3-70b-versatile", 
    temperature=0.1 
)

@app.post("/ask")
async def ask_bot(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        
        # 1. First, check Supabase for Semantic Match
        query_vector = get_embedding(user_input)
        rpc_res = supabase.rpc("match_knowledge", {
            "query_embedding": query_vector,
            "match_threshold": 0.8,
            "match_count": 1
        }).execute()

        if rpc_res.data:
            return {"answer": rpc_res.data[0]['answer']}
        
        # 2. If not in DB, fallback to text file + Groq
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            context = f.read()[:8000]
            
        prompt = ChatPromptTemplate.from_template("Context: {context}\n\nUser: {input}\nAnswer:")
        full_prompt = prompt.format(context=context, input=user_input)
        response = llm.invoke(full_prompt)
        
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"System Error: {str(e)}"}