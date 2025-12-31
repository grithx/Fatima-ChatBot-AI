# # # # # # # # # # # # # # # # import streamlit as st
# # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # Page Configuration
# # # # # # # # # # # # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # # # # # # # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # # # # # # # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # # # # # # # # # # # Load Environment Variables
# # # # # # # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # # # # # # Sidebar for Status
# # # # # # # # # # # # # # # # with st.sidebar:
# # # # # # # # # # # # # # # #     st.header("System Status")
# # # # # # # # # # # # # # # #     if os.path.exists("./db"):
# # # # # # # # # # # # # # # #         st.success("Database: Connected")
# # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # #         st.error("Database: Not Found! Run ingest.py first.")
    
# # # # # # # # # # # # # # # #     if st.button("Clear Chat History"):
# # # # # # # # # # # # # # # #         st.session_state.messages = []

# # # # # # # # # # # # # # # # # Initialize Models (Cached for speed)
# # # # # # # # # # # # # # # # @st.cache_resource
# # # # # # # # # # # # # # # # def load_rag_system():
# # # # # # # # # # # # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # # # # # # # # # # # #     llm = ChatGroq(
# # # # # # # # # # # # # # # #         groq_api_key=os.getenv("GROQ_API_KEY"),
# # # # # # # # # # # # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # # # # # # # # # # # #         temperature=0.2
# # # # # # # # # # # # # # # #     )
# # # # # # # # # # # # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # #     Context: {context}
# # # # # # # # # # # # # # # #     Question: {input}
# # # # # # # # # # # # # # # #     Answer:""")
    
# # # # # # # # # # # # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # # # # # # chain = load_rag_system()

# # # # # # # # # # # # # # # # # Chat History Setup
# # # # # # # # # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # # # # # # # # #     st.session_state.messages = []

# # # # # # # # # # # # # # # # # Display chat messages from history
# # # # # # # # # # # # # # # # for message in st.session_state.messages:
# # # # # # # # # # # # # # # #     with st.chat_message(message["role"]):
# # # # # # # # # # # # # # # #         st.markdown(message["content"])

# # # # # # # # # # # # # # # # # User Input
# # # # # # # # # # # # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # # # # # # # # # # # #     # Add user message to history
# # # # # # # # # # # # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # # # # # # # # # # #     with st.chat_message("user"):
# # # # # # # # # # # # # # # #         st.markdown(prompt)

# # # # # # # # # # # # # # # #     # Generate Response
# # # # # # # # # # # # # # # #     with st.chat_message("assistant"):
# # # # # # # # # # # # # # # #         with st.spinner("Thinking..."):
# # # # # # # # # # # # # # # #             response = chain.invoke({"input": prompt})
# # # # # # # # # # # # # # # #             full_response = response["answer"]
# # # # # # # # # # # # # # # #             st.markdown(full_response)
    
# # # # # # # # # # # # # # # #     # Add assistant response to history
# # # # # # # # # # # # # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})





# # # # # # # # # # # # # # # # -------------------------------------------------------------------------
# # # # # # # # # # # # # # # # CRITICAL FIX: This must be the very first code in the file
# # # # # # # # # # # # # # # # This swaps the system sqlite3 with pysqlite3-binary for ChromaDB support
# # # # # # # # # # # # # # # # __import__('pysqlite3')
# # # # # # # # # # # # # # # # import sys
# # # # # # # # # # # # # # # # sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # # # # # -------------------------------------------------------------------------

# # # # # # # # # # # # # # # import streamlit as st
# # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # Page Configuration
# # # # # # # # # # # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # # # # # # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # # # # # # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # # # # # # # # # # Load Environment Variables (Try .env first, fallback to st.secrets)
# # # # # # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # # # # # Securely get API Key
# # # # # # # # # # # # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # # # # # # # # # # # if not groq_api_key and "GROQ_API_KEY" in st.secrets:
# # # # # # # # # # # # # # #     groq_api_key = st.secrets["GROQ_API_KEY"]

# # # # # # # # # # # # # # # if not groq_api_key:
# # # # # # # # # # # # # # #     st.error("⚠️ GROQ_API_KEY is missing! Please add it to .env or Streamlit Secrets.")
# # # # # # # # # # # # # # #     st.stop()

# # # # # # # # # # # # # # # # Sidebar for Status
# # # # # # # # # # # # # # # db_path = "./db"
# # # # # # # # # # # # # # # db_exists = os.path.exists(db_path) and os.listdir(db_path)

# # # # # # # # # # # # # # # with st.sidebar:
# # # # # # # # # # # # # # #     st.header("System Status")
# # # # # # # # # # # # # # #     if db_exists:
# # # # # # # # # # # # # # #         st.success("Database: Connected")
# # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # #         st.error("Database: Not Found!")
# # # # # # # # # # # # # # #         st.warning("⚠️ Please run `ingest.py` locally and commit the `db` folder to GitHub.")
    
# # # # # # # # # # # # # # #     if st.button("Clear Chat History"):
# # # # # # # # # # # # # # #         st.session_state.messages = []
# # # # # # # # # # # # # # #         st.rerun()

# # # # # # # # # # # # # # # # Initialize Models (Cached for speed)
# # # # # # # # # # # # # # # @st.cache_resource
# # # # # # # # # # # # # # # def load_rag_system():
# # # # # # # # # # # # # # #     # Only load if DB exists to avoid crashing
# # # # # # # # # # # # # # #     if not os.path.exists(db_path):
# # # # # # # # # # # # # # #         return None

# # # # # # # # # # # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
# # # # # # # # # # # # # # #     # Initialize Chroma
# # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
# # # # # # # # # # # # # # #     llm = ChatGroq(
# # # # # # # # # # # # # # #         groq_api_key=groq_api_key,
# # # # # # # # # # # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # # # # # # # # # # #         temperature=0.2
# # # # # # # # # # # # # # #     )
    
# # # # # # # # # # # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # #     Use the following pieces of retrieved context to answer the question. 
# # # # # # # # # # # # # # #     If you don't know the answer, just say that you don't know. 
    
# # # # # # # # # # # # # # #     Context: {context}
    
# # # # # # # # # # # # # # #     Question: {input}
# # # # # # # # # # # # # # #     Answer:""")
    
# # # # # # # # # # # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # # # # # # Load the chain
# # # # # # # # # # # # # # # if db_exists:
# # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # #         chain = load_rag_system()
# # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # #         st.error(f"Error loading model: {e}")
# # # # # # # # # # # # # # #         chain = None
# # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # #     chain = None

# # # # # # # # # # # # # # # # Chat History Setup
# # # # # # # # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # # # # # # # #     st.session_state.messages = []

# # # # # # # # # # # # # # # # Display chat messages from history
# # # # # # # # # # # # # # # for message in st.session_state.messages:
# # # # # # # # # # # # # # #     with st.chat_message(message["role"]):
# # # # # # # # # # # # # # #         st.markdown(message["content"])

# # # # # # # # # # # # # # # # User Input
# # # # # # # # # # # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # # # # # # # # # # #     # Add user message to history
# # # # # # # # # # # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # # # # # # # # # #     with st.chat_message("user"):
# # # # # # # # # # # # # # #         st.markdown(prompt)

# # # # # # # # # # # # # # #     # Check if system is ready
# # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # #         st.error("The AI Brain is not loaded. Please ensure the database is generated and uploaded.")
# # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # #         # Generate Response
# # # # # # # # # # # # # # #         with st.chat_message("assistant"):
# # # # # # # # # # # # # # #             with st.spinner("Searching knowledge base..."):
# # # # # # # # # # # # # # #                 try:
# # # # # # # # # # # # # # #                     response = chain.invoke({"input": prompt})
# # # # # # # # # # # # # # #                     full_response = response["answer"]
# # # # # # # # # # # # # # #                     st.markdown(full_response)
                    
# # # # # # # # # # # # # # #                     # Add assistant response to history
# # # # # # # # # # # # # # #                     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # # # # # # # # # # # #                 except Exception as e:
# # # # # # # # # # # # # # #                     st.error(f"An error occurred: {str(e)}")



# # # # # # # # # # # # # # # node js conversion



# # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # CORS allow karein taake frontend connect ho sake
# # # # # # # # # # # # # # app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# # # # # # # # # # # # # # # Load RAG System
# # # # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # # # # # # # # # # vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # # # # # # # # # # llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile", temperature=0.2)

# # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # #     response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # #     return {"answer": response["answer"]}



# # # # # # # # # # # # # # update the path of the db becuase we have move the app.py into the api folder


# # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # import os
# # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # Environment variables load karein
# # # # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # CORS settings: Taake aapka frontend backend se asani se baat kar sake
# # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # )

# # # # # # # # # # # # # # --- Path Correction ---
# # # # # # # # # # # # # # Chunkay ye file 'api' folder mein hai, humein '../db' use karna hoga 
# # # # # # # # # # # # # # taake code ek step piche ja kar 'db' folder ko dhund sakay.
# # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # # Load RAG System
# # # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # # # # # # Vector Database check aur connection
# # # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # # else:
# # # # # # # # # # # # #     print(f"Warning: Database folder not found at {DB_PATH}")
# # # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # )

# # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # Use the provided context to answer the user's question accurately.
# # # # # # # # # # # # # If you don't know the answer, politely say so.

# # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # Chain Setup
# # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # # # # # # if vector_db:
# # # # # # # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # # # # # # else:
# # # # # # # # # # # # #     chain = None

# # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # #         return {"answer": "Error: AI database not found. Please check paths."}
        
# # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # #     user_input = data.get("message")
    
# # # # # # # # # # # # #     try:
# # # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # #         return {"answer": f"Sorry, an error occurred: {str(e)}"}




# # # # # # # # # # # # # update the code to fix the crash isssue of chatbot


# # # # # # # # # # # # # --- SQLite Fix (Deployment ke liye zaroori) ---
# # # # # # # # # # # # try:
# # # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # # #     import sys
# # # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # except ImportError:
# # # # # # # # # # # #     pass 

# # # # # # # # # # # # import os
# # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # )

# # # # # # # # # # # # # --- Path Handling ---
# # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # Load Models
# # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # # # # # Database Connect
# # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # else:
# # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # )

# # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # # # # # if vector_db:
# # # # # # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # # # # # else:
# # # # # # # # # # # #     chain = None

# # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # #     if not chain:
# # # # # # # # # # # #         return {"answer": "Error: Database folder not found. Please ensure 'db' folder is uploaded."}
    
# # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # #     user_input = data.get("message")
    
# # # # # # # # # # # #     try:
# # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}


# # # # # # # # # # # # Vercel par 250 MB ki limit exceed hone ki sab se bari wajah langchain-huggingface library hai, kyunke ye apne saath PyTorch aur heavy models download karti hai. Isay bypass karne ke liye humein "Lightweight" approach apnaani hogi.

# # # # # # # # # # # # Niche diya gaya code aapke api/app.py ko optimize kar dega taake size kam ho jaye:




# # # # # # # # # # # try:
# # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # #     import sys
# # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # except ImportError:
# # # # # # # # # # #     pass 

# # # # # # # # # # # import os
# # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # from dotenv import load_dotenv

# # # # # # # # # # # # Lightweight Embeddings and Components
# # # # # # # # # # # from langchain_community.embeddings import HealthcareHuggingFaceEmbeddings # Ya niche wala alternative
# # # # # # # # # # # from langchain_community.embeddings import HuggingFaceEmbeddings 
# # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # load_dotenv()
# # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # app.add_middleware(
# # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # )

# # # # # # # # # # # # --- Path Handling ---
# # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # Load Models - optimized for size
# # # # # # # # # # # # Note: all-MiniLM-L6-v2 is small, but the library matters
# # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # # # # Database Connect
# # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # else:
# # # # # # # # # # #     vector_db = None

# # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # )

# # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # Context: {context}
# # # # # # # # # # # Question: {input}
# # # # # # # # # # # Answer:""")

# # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # # # # if vector_db:
# # # # # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # # # # else:
# # # # # # # # # # #     chain = None

# # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # #     if not chain:
# # # # # # # # # # #         return {"answer": "Error: Database folder not found."}
    
# # # # # # # # # # #     data = await request.json()
# # # # # # # # # # #     user_input = data.get("message")
    
# # # # # # # # # # #     try:
# # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # #     except Exception as e:
# # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # # # # try:
# # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # #     import sys
# # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # except ImportError:
# # # # # # # # # # #     pass 

# # # # # # # # # # # import os
# # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # load_dotenv()
# # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # app.add_middleware(
# # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # )

# # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # Memory-efficient embeddings
# # # # # # # # # # # embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # else:
# # # # # # # # # # #     vector_db = None

# # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # )

# # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # Context: {context}
# # # # # # # # # # # Question: {input}
# # # # # # # # # # # Answer:""")

# # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # #     if not chain:
# # # # # # # # # # #         return {"answer": "Error: Database folder not found."}
# # # # # # # # # # #     data = await request.json()
# # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # #     try:
# # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # #     except Exception as e:
# # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # # # try:
# # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # #     import sys
# # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # except ImportError:
# # # # # # # # # #     pass 

# # # # # # # # # # import os
# # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # load_dotenv()
# # # # # # # # # # app = FastAPI()

# # # # # # # # # # app.add_middleware(
# # # # # # # # # #     CORSMiddleware,
# # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # #     allow_credentials=True,
# # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # )

# # # # # # # # # # # Path Handling
# # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # Wahi embeddings jo database banate waqt use kiye
# # # # # # # # # # embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # else:
# # # # # # # # # #     vector_db = None

# # # # # # # # # # llm = ChatGroq(
# # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # #     temperature=0.2
# # # # # # # # # # )

# # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # Context: {context}
# # # # # # # # # # Question: {input}
# # # # # # # # # # Answer:""")

# # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# # # # # # # # # # @app.post("/ask")
# # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # #     if not chain:
# # # # # # # # # #         return {"answer": "Error: Database folder not found."}
# # # # # # # # # #     data = await request.json()
# # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # #     try:
# # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}
    


# # # # # # # # # # ye code bina kisi local embedding model ke chahay ga. Ye seedha text file (zt_data.txt) ko read karega aur Groq ko bhej dega. Ye 100% 250MB se kam hoga.


# # # # # # # # # import os
# # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # # # load_dotenv()
# # # # # # # # # app = FastAPI()

# # # # # # # # # app.add_middleware(
# # # # # # # # #     CORSMiddleware,
# # # # # # # # #     allow_origins=["*"],
# # # # # # # # #     allow_credentials=True,
# # # # # # # # #     allow_methods=["*"],
# # # # # # # # #     allow_headers=["*"],
# # # # # # # # # )

# # # # # # # # # # Knowledge Base Read Karein
# # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")

# # # # # # # # # def get_context():
# # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # #             return f.read()[:10000] # Pehle 10k characters (Vercel limits ke liye)
# # # # # # # # #     return "No hosting info available."

# # # # # # # # # llm = ChatGroq(
# # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # #     temperature=0.2
# # # # # # # # # )

# # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # Use the following context to answer:
# # # # # # # # # {context}

# # # # # # # # # User Question: {input}
# # # # # # # # # Answer:""")

# # # # # # # # # @app.post("/ask")
# # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # #     data = await request.json()
# # # # # # # # #     user_input = data.get("message")
# # # # # # # # #     context = get_context()
    
# # # # # # # # #     try:
# # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # #         response = llm.invoke(full_prompt)
# # # # # # # # #         return {"answer": response.content}
# # # # # # # # #     except Exception as e:
# # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # import os
# # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # from fastapi.responses import HTMLResponse # Naya import
# # # # # # # # from dotenv import load_dotenv
# # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # # load_dotenv()
# # # # # # # # app = FastAPI()

# # # # # # # # app.add_middleware(
# # # # # # # #     CORSMiddleware,
# # # # # # # #     allow_origins=["*"],
# # # # # # # #     allow_credentials=True,
# # # # # # # #     allow_methods=["*"],
# # # # # # # #     allow_headers=["*"],
# # # # # # # # )

# # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html") # HTML ka path

# # # # # # # # # --- Naya Route: Chatbot ka Page dikhane ke liye ---
# # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # async def get_index():
# # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # #             return f.read()
# # # # # # # #     return "<h1>Index.html not found in templates/</h1>"

# # # # # # # # def get_context():
# # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # #             return f.read()[:10000]
# # # # # # # #     return "No hosting info available."

# # # # # # # # llm = ChatGroq(
# # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # #     temperature=0.2
# # # # # # # # )

# # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # Use the following context to answer:
# # # # # # # # {context}

# # # # # # # # User Question: {input}
# # # # # # # # Answer:""")

# # # # # # # # @app.post("/ask")
# # # # # # # # async def ask_bot(request: Request):
# # # # # # # #     data = await request.json()
# # # # # # # #     user_input = data.get("message")
# # # # # # # #     context = get_context()
# # # # # # # #     try:
# # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # #         response = llm.invoke(full_prompt)
# # # # # # # #         return {"answer": response.content}
# # # # # # # #     except Exception as e:
# # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # import os
# # # # # # # from fastapi import FastAPI, Request
# # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # from dotenv import load_dotenv
# # # # # # # from langchain_groq import ChatGroq
# # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # load_dotenv()
# # # # # # # app = FastAPI()

# # # # # # # app.add_middleware(
# # # # # # #     CORSMiddleware,
# # # # # # #     allow_origins=["*"],
# # # # # # #     allow_credentials=True,
# # # # # # #     allow_methods=["*"],
# # # # # # #     allow_headers=["*"],
# # # # # # # )

# # # # # # # # Path settings
# # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # Aapki index.html ka sahi path
# # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# # # # # # # # 🏠 Home Route: Ye aapka interface dikhayega
# # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # async def get_home():
# # # # # # #     try:
# # # # # # #         if os.path.exists(HTML_PATH):
# # # # # # #             with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # #                 return f.read()
# # # # # # #         return "<h1>Error: templates/index.html not found!</h1>"
# # # # # # #     except Exception as e:
# # # # # # #         return f"<h1>Internal Error: {str(e)}</h1>"

# # # # # # # # 🤖 AI Logic
# # # # # # # def get_context():
# # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # #             return f.read()[:10000]
# # # # # # #     return "No hosting info available."

# # # # # # # llm = ChatGroq(
# # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # #     temperature=0.2
# # # # # # # )

# # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # Use the following context to answer the user:
# # # # # # # {context}

# # # # # # # User Question: {input}
# # # # # # # Answer:""")

# # # # # # # # 💬 API Route: Ye chat ka jawab dega
# # # # # # # @app.post("/ask")
# # # # # # # async def ask_bot(request: Request):
# # # # # # #     data = await request.json()
# # # # # # #     user_input = data.get("message")
# # # # # # #     context = get_context()
# # # # # # #     try:
# # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # #         response = llm.invoke(full_prompt)
# # # # # # #         return {"answer": response.content}
# # # # # # #     except Exception as e:
# # # # # # #         return {"answer": f"AI Error: {str(e)}"}


# # # # # # # update code to give the Bilkul, ye raha aapka complete updated api/app.py. Maine is mein aapka naya professional prompt, temperature settings, aur file paths ko organize kar diya hai taake bot bilkul to-the-point jawab de.



# # # # import os
# # # # from fastapi import FastAPI, Request
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from fastapi.responses import HTMLResponse
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

# # # # # --- Path Settings ---
# # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# # # # # --- UI Route ---
# # # # @app.get("/", response_class=HTMLResponse)
# # # # async def get_home():
# # # #     try:
# # # #         if os.path.exists(HTML_PATH):
# # # #             with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # #                 return f.read()
# # # #         return "<h1>Error: templates/index.html not found!</h1>"
# # # #     except Exception as e:
# # # #         return f"<h1>Internal Error: {str(e)}</h1>"

# # # # # --- AI Logic & Professional Prompting ---
# # # # def get_context():
# # # #     if os.path.exists(DATA_PATH):
# # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # #             # Context window limit to avoid token overflow
# # # #             return f.read()[:8000]
# # # #     return "No hosting info available."

# # # # # Low temperature (0.1) keeps the bot factual and avoids 'hallucinations'
# # # # llm = ChatGroq(
# # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # #     model_name="llama-3.3-70b-versatile", 
# # # #     temperature=0.1 
# # # # )

# # # # # Professional & Structured Prompt
# # # # prompt = ChatPromptTemplate.from_template("""
# # # # You are the Official ZT Hosting Support AI. Your goal is to provide concise, professional, and structured information.

# # # # STRICT GUIDELINES:
# # # # 1. ONLY use information from the provided context. If not found, say you don't know politely.
# # # # 2. BE CONCISE: Answer directly. No "Hello", "I hope you're well", or long intros. 
# # # # 3. FORMATTING: Use **bold** for prices and plan names. Use bullet points for features.
# # # # 4. STRUCTURE: Responses must be highly organized. Use tables for plan comparisons.
# # # # 5. NO EXTRA INFO: Do not suggest other plans unless requested.
# # # # 6. LANGUAGE: If the question is in Roman Urdu, respond in Roman Urdu with this same professional structure.

# # # # Context:
# # # # {context}

# # # # User Question: {input}
# # # # Answer:""")

# # # # # --- Chat API Route ---
# # # # @app.post("/ask")
# # # # async def ask_bot(request: Request):
# # # #     try:
# # # #         data = await request.json()
# # # #         user_input = data.get("message")
        
# # # #         if not user_input:
# # # #             return {"answer": "Please provide a message."}

# # # #         context = get_context()
        
# # # #         # Generating structured response
# # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # #         response = llm.invoke(full_prompt)
        
# # # #         return {"answer": response.content}
    
# # # #     except Exception as e:
# # # #         return {"answer": f"System Error: {str(e)}"}



# # # # # # Aapki app.py FastAPI use kar rahi hai, jo ke bohat achi baat hai kyunki ye Flask se fast hai. Ab hum isi file mein Admin Side logic aur Supabase Vector Search ko integrate karenge.



# # # # # import os
# # # # # import requests
# # # # # from fastapi import FastAPI, Request, Depends, HTTPException
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from fastapi.responses import HTMLResponse
# # # # # from fastapi.security import HTTPBasic, HTTPBasicCredentials
# # # # # from dotenv import load_dotenv
# # # # # from langchain_groq import ChatGroq
# # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # from supabase import create_client

# # # # # load_dotenv()
# # # # # app = FastAPI()
# # # # # security = HTTPBasic()

# # # # # # --- Security: Admin Authentication ---
# # # # # def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
# # # # #     correct_username = "admin"
# # # # #     correct_password = "eagale123" # Sir ke liye password
# # # # #     if credentials.username != correct_username or credentials.password != correct_password:
# # # # #         raise HTTPException(status_code=401, detail="Invalid Credentials")
# # # # #     return credentials.username

# # # # # # --- Middleware & Database ---
# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # --- Path Settings ---
# # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # # # # --- Helpers: Vector Generation ---
# # # # # def get_embedding(text):
# # # # #     # HuggingFace API use kar ke text ko numbers (vectors) mein badalna
# # # # #     api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
# # # # #     headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
# # # # #     response = requests.post(api_url, headers=headers, json={"inputs": text})
# # # # #     return response.json()

# # # # # # --- UI Routes ---
# # # # # @app.get("/", response_class=HTMLResponse)
# # # # # async def get_home():
# # # # #     if os.path.exists(HTML_PATH):
# # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return "<h1>Error: templates/index.html not found!</h1>"

# # # # # @app.get("/eagale-admin-secret", response_class=HTMLResponse)
# # # # # async def get_admin(username: str = Depends(authenticate)):
# # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # # # # --- Admin API: Data Save to DB ---
# # # # # @app.post("/admin/add-to-db")
# # # # # async def save_to_db(request: Request, username: str = Depends(authenticate)):
# # # # #     data = await request.json()
# # # # #     q, a = data.get("question"), data.get("answer")
# # # # #     vector = get_embedding(q)
    
# # # # #     supabase.table("bot_knowledge").insert({
# # # # #         "question": q, 
# # # # #         "answer": a, 
# # # # #         "embedding": vector
# # # # #     }).execute()
    
# # # # #     return {"message": "Success! Database updated."}

# # # # # # --- AI Logic & Chat API ---
# # # # # llm = ChatGroq(
# # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # #     model_name="llama-3.3-70b-versatile", 
# # # # #     temperature=0.1 
# # # # # )

# # # # # @app.post("/ask")
# # # # # async def ask_bot(request: Request):
# # # # #     try:
# # # # #         data = await request.json()
# # # # #         user_input = data.get("message")
        
# # # # #         # 1. First, check Supabase for Semantic Match
# # # # #         query_vector = get_embedding(user_input)
# # # # #         rpc_res = supabase.rpc("match_knowledge", {
# # # # #             "query_embedding": query_vector,
# # # # #             "match_threshold": 0.8,
# # # # #             "match_count": 1
# # # # #         }).execute()

# # # # #         if rpc_res.data:
# # # # #             return {"answer": rpc_res.data[0]['answer']}
        
# # # # #         # 2. If not in DB, fallback to text file + Groq
# # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # #             context = f.read()[:8000]
            
# # # # #         prompt = ChatPromptTemplate.from_template("Context: {context}\n\nUser: {input}\nAnswer:")
# # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # #         response = llm.invoke(full_prompt)
        
# # # # #         return {"answer": response.content}
# # # # #     except Exception as e:
# # # # #         return {"answer": f"System Error: {str(e)}"}


# # # # # add safety check for not crashing the chatbot

# # # # # import os
# # # # # import requests
# # # # # from fastapi import FastAPI, Request, Depends, HTTPException
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from fastapi.responses import HTMLResponse
# # # # # from fastapi.security import HTTPBasic, HTTPBasicCredentials
# # # # # from dotenv import load_dotenv
# # # # # from langchain_groq import ChatGroq
# # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # from supabase import create_client

# # # # # load_dotenv()
# # # # # app = FastAPI()
# # # # # security = HTTPBasic()

# # # # # # --- Security: Admin Authentication ---
# # # # # def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
# # # # #     if credentials.username != "admin" or credentials.password != "eagale123":
# # # # #         raise HTTPException(status_code=401, detail="Invalid Credentials")
# # # # #     return credentials.username

# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # # Initialize Supabase Safely
# # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# # # # # # Path Settings
# # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")
# # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")

# # # # # def get_embedding(text):
# # # # #     try:
# # # # #         api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
# # # # #         headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
# # # # #         response = requests.post(api_url, headers=headers, json={"inputs": text}, timeout=10)
# # # # #         res_data = response.json()
# # # # #         if isinstance(res_data, list):
# # # # #             return res_data
# # # # #         return [0] * 384 # Fallback vector if HF fails
# # # # #     except:
# # # # #         return [0] * 384

# # # # # @app.get("/", response_class=HTMLResponse)
# # # # # async def get_home():
# # # # #     if os.path.exists(HTML_PATH):
# # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return "<h1>Templates folder not found!</h1>"

# # # # # @app.get("/eagale-admin-secret", response_class=HTMLResponse)
# # # # # async def get_admin(username: str = Depends(authenticate)):
# # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return "<h1>Admin Template not found!</h1>"

# # # # # @app.post("/admin/add-to-db")
# # # # # async def save_to_db(request: Request, username: str = Depends(authenticate)):
# # # # #     data = await request.json()
# # # # #     q, a = data.get("question"), data.get("answer")
# # # # #     vector = get_embedding(q)
# # # # #     if supabase:
# # # # #         supabase.table("bot_knowledge").insert({"question": q, "answer": a, "embedding": vector}).execute()
# # # # #     return {"message": "Database updated."}

# # # # # @app.post("/ask")
# # # # # async def ask_bot(request: Request):
# # # # #     try:
# # # # #         data = await request.json()
# # # # #         user_input = data.get("message")
        
# # # # #         # Semantic Search with Supabase
# # # # #         if supabase:
# # # # #             query_vector = get_embedding(user_input)
# # # # #             rpc_res = supabase.rpc("match_knowledge", {
# # # # #                 "query_embedding": query_vector,
# # # # #                 "match_threshold": 0.8,
# # # # #                 "match_count": 1
# # # # #             }).execute()
# # # # #             if rpc_res.data:
# # # # #                 return {"answer": rpc_res.data[0]['answer']}

# # # # #         # Fallback to Text File
# # # # #         context = ""
# # # # #         if os.path.exists(DATA_PATH):
# # # # #             with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # #                 context = f.read()[:8000]

# # # # #         llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile", temperature=0.1)
# # # # #         prompt = ChatPromptTemplate.from_template("Context: {context}\n\nUser: {input}\nAnswer:")
# # # # #         response = llm.invoke(prompt.format(context=context, input=user_input))
# # # # #         return {"answer": response.content}
# # # # #     except Exception as e:
# # # # #         return {"answer": f"Error: {str(e)}"}



# # # # update code to add the admin path admin website ka path add kea ha 
# # # import os 
# # # import json
# # # from fastapi import FastAPI, Request
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.responses import HTMLResponse
# # # from dotenv import load_dotenv
# # # from langchain_groq import ChatGroq
# # # from langchain_core.prompts import ChatPromptTemplate
# # # from supabase import create_client, Client # Naya import

# # # load_dotenv()
# # # app = FastAPI()

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # --- Path Settings ---
# # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # # --- Supabase Setup ---
# # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # --- UI Routes ---
# # # @app.get("/", response_class=HTMLResponse)
# # # async def get_home():
# # #     if os.path.exists(HTML_PATH):
# # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # #             return f.read()
# # #     return "<h1>Error: templates/index.html not found!</h1>"

# # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # async def get_admin():
# # #     if os.path.exists(ADMIN_HTML_PATH):
# # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # #             return f.read()
# # #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # # --- Admin API: Save to Supabase ---
# # # @app.post("/add-faq")
# # # async def add_faq(request: Request):
# # #     try:
# # #         data = await request.json()
# # #         q = data.get("question").strip().lower()
# # #         a = data.get("answer").strip()
        
# # #         # Supabase mein insert
# # #         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # #         return {"status": "success"}
# # #     except Exception as e:
# # #         return {"status": "error", "message": str(e)}

# # # # --- AI Logic ---
# # # def get_context():
# # #     if os.path.exists(DATA_PATH):
# # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # #             return f.read()[:8000]
# # #     return "No hosting info available."

# # # llm = ChatGroq(
# # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # #     model_name="llama-3.3-70b-versatile", 
# # #     temperature=0.1 
# # # )

# # # prompt = ChatPromptTemplate.from_template("""
# # # You are the Official ZT Hosting Support AI.
# # # STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# # # Context: {context}
# # # User Question: {input}
# # # Answer:""")

# # # # --- Chat API Route (Priority: DB -> File/AI) ---
# # # @app.post("/ask")
# # # async def ask_bot(request: Request):
# # #     try:
# # #         data = await request.json()
# # #         user_input = data.get("message", "").strip().lower()
        
# # #         if not user_input:
# # #             return {"answer": "Please provide a message."}

# # #         # STEP 1: Check Supabase Database first
# # #         db_query = supabase.table("manual_faqs").select("answer").eq("question", user_input).execute()
        
# # #         if db_query.data:
# # #             # Agar exact match mil gaya to AI ke paas nahi jayenge
# # #             return {"answer": db_query.data[0]['answer']}

# # #         # STEP 2: Fallback to AI + Website Context
# # #         context = get_context()
# # #         full_prompt = prompt.format(context=context, input=user_input)
# # #         response = llm.invoke(full_prompt)
        
# # #         return {"answer": response.content}
    
# # #     except Exception as e:
# # #         return {"answer": f"System Error: {str(e)}"}




# # # Bilkul, aapka current code bilkul sahi track par hai. Main is mein sirf Smart Search (Semantic matching) aur Delete functionality add kar raha hoon taake bot behtar kaam kare aur Admin Panel professional ho jaye.

# # # Aapka existing logic (Priority: DB -> AI) bilkul mehfooz hai.



# # import os 
# # import json
# # from fastapi import FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse
# # from dotenv import load_dotenv
# # from langchain_groq import ChatGroq
# # from langchain_core.prompts import ChatPromptTemplate
# # from supabase import create_client, Client 

# # load_dotenv()
# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # --- Path Settings ---
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # --- Supabase Setup ---
# # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # --- UI Routes ---
# # @app.get("/", response_class=HTMLResponse)
# # async def get_home():
# #     if os.path.exists(HTML_PATH):
# #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# #             return f.read()
# #     return "<h1>Error: templates/index.html not found!</h1>"

# # @app.get("/admin-zt", response_class=HTMLResponse)
# # async def get_admin():
# #     if os.path.exists(ADMIN_HTML_PATH):
# #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# #             return f.read()
# #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # --- Admin API: Save, Get, and Delete ---
# # @app.post("/add-faq")
# # async def add_faq(request: Request):
# #     try:
# #         data = await request.json()
# #         q = data.get("question").strip().lower()
# #         a = data.get("answer").strip()
# #         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# #         return {"status": "success"}
# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}

# # @app.get("/get-faqs")
# # async def get_faqs():
# #     # Admin panel par list dikhane ke liye
# #     response = supabase.table("manual_faqs").select("*").execute()
# #     return response.data

# # @app.delete("/delete-faq/{faq_id}")
# # async def delete_faq(faq_id: int):
# #     try:
# #         supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
# #         return {"status": "success"}
# #     except Exception as e:
# #         return {"status": "error", "message": str(e)}

# # # --- AI Logic ---
# # def get_context():
# #     if os.path.exists(DATA_PATH):
# #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# #             return f.read()[:8000]
# #     return "No hosting info available."

# # llm = ChatGroq(
# #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# #     model_name="llama-3.3-70b-versatile", 
# #     temperature=0.1 
# # )

# # prompt = ChatPromptTemplate.from_template("""
# # You are the Official ZT Hosting Support AI.
# # STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# # Context: {context}
# # User Question: {input}
# # Answer:""")

# # @app.post("/ask")
# # async def ask_bot(request: Request):
# #     try:
# #         data = await request.json()
# #         user_input = data.get("message", "").strip()
        
# #         if not user_input:
# #             return {"answer": "Please provide a message."}

# #         # 1. DB se saare sawal mangwao
# #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# #         db_data = db_res.data

# #         if db_data:
# #             # DB ke saare sawalon ki list banao
# #             db_questions = [row['question'] for row in db_data]
            
# #             # AI se pucho ke kya user ka sawal DB mein mojud kisi sawal se milta hai
# #             verification_prompt = f"""
# #             User Question: "{user_input}"
# #             Available FAQs: {db_questions}
            
# #             Task: Does the User Question have the same meaning as any of the Available FAQs? 
# #             - If YES, return ONLY the exact matching question from the list.
# #             - If NO, return 'NO_MATCH'.
# #             Return only the text, no explanation.
# #             """
            
# #             match_check = llm.invoke(verification_prompt)
# #             matched_q = match_check.content.strip()

# #             # Agar AI ko koi milta julta sawal mil gaya
# #             if "NO_MATCH" not in matched_q:
# #                 for row in db_data:
# #                     if row['question'].lower() in matched_q.lower():
# #                         return {"answer": row['answer']}

# #         # 2. Agar DB mein match nahi mila, to normal AI + File process
# #         context = get_context()
# #         full_prompt = prompt.format(context=context, input=user_input)
# #         response = llm.invoke(full_prompt)
        
# #         return {"answer": response.content}
    
# #     except Exception as e:
# #         return {"answer": f"System Error: {str(e)}"}



# # Bilkul, main aapke existing logic ko bilkul nahi cheron ga. Bas ooper security functions add karoon ga aur aapke Admin routes mein Depends(authenticate) laga doon ga taake ye secure ho jayein.

# # Ye raha aapka updated code:


# import os 
# import json
# import secrets # New for security
# from fastapi import FastAPI, Request, Depends, HTTPException, status # Added dependencies
# from fastapi.security import HTTPBasic, HTTPBasicCredentials # Added for security
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from supabase import create_client, Client 

# load_dotenv()
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Security Settings ---
# security = HTTPBasic()
# ADMIN_USERNAME = "admin"
# ADMIN_PASSWORD = "ZT_Password_123" # <--- Isay aap change kar sakte hain

# def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
#     is_username_correct = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
#     is_password_correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
#     if not (is_username_correct and is_password_correct):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username

# # --- Path Settings ---
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # --- Supabase Setup ---
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # --- UI Routes ---
# @app.get("/", response_class=HTMLResponse)
# async def get_home():
#     if os.path.exists(HTML_PATH):
#         with open(HTML_PATH, "r", encoding="utf-8") as f:
#             return f.read()
#     return "<h1>Error: templates/index.html not found!</h1>"

# # Yahan Depends add kiya gaya hai
# @app.get("/admin-zt", response_class=HTMLResponse)
# async def get_admin(username: str = Depends(authenticate)):
#     if os.path.exists(ADMIN_HTML_PATH):
#         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
#             return f.read()
#     return "<h1>Error: templates/admin.html not found!</h1>"

# # --- Admin API: Save, Get, and Delete (All Secured) ---
# @app.post("/add-faq")
# async def add_faq(request: Request, username: str = Depends(authenticate)):
#     try:
#         data = await request.json()
#         q = data.get("question").strip().lower()
#         a = data.get("answer").strip()
#         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
#         return {"status": "success"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# @app.get("/get-faqs")
# async def get_faqs(username: str = Depends(authenticate)):
#     response = supabase.table("manual_faqs").select("*").execute()
#     return response.data

# @app.delete("/delete-faq/{faq_id}")
# async def delete_faq(faq_id: int, username: str = Depends(authenticate)):
#     try:
#         supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
#         return {"status": "success"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# # --- AI Logic (No Changes Here) ---
# def get_context():
#     if os.path.exists(DATA_PATH):
#         with open(DATA_PATH, "r", encoding="utf-8") as f:
#             return f.read()[:8000]
#     return "No hosting info available."

# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="llama-3.3-70b-versatile", 
#     temperature=0.1 
# )

# prompt = ChatPromptTemplate.from_template("""
# You are the Official ZT Hosting Support AI.
# STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# Context: {context}
# User Question: {input}
# Answer:""")

# @app.post("/ask")
# async def ask_bot(request: Request):
#     try:
#         data = await request.json()
#         user_input = data.get("message", "").strip()
        
#         if not user_input:
#             return {"answer": "Please provide a message."}

#         db_res = supabase.table("manual_faqs").select("question, answer").execute()
#         db_data = db_res.data

#         if db_data:
#             db_questions = [row['question'] for row in db_data]
            
#             verification_prompt = f"""
#             User Question: "{user_input}"
#             Available FAQs: {db_questions}
            
#             Task: Does the User Question have the same meaning as any of the Available FAQs? 
#             - If YES, return ONLY the exact matching question from the list.
#             - If NO, return 'NO_MATCH'.
#             Return only the text, no explanation.
#             """
            
#             match_check = llm.invoke(verification_prompt)
#             matched_q = match_check.content.strip()

#             if "NO_MATCH" not in matched_q:
#                 for row in db_data:
#                     if row['question'].lower() in matched_q.lower():
#                         return {"answer": row['answer']}

#         context = get_context()
#         full_prompt = prompt.format(context=context, input=user_input)
#         response = llm.invoke(full_prompt)
        
#         return {"answer": response.content}
    
#     except Exception as e:
#         return {"answer": f"System Error: {str(e)}"}



# Bilkul, maine aapka diya hua security code aur aapki purani AI logic (Semantic Search wali) dono ko merge kar diya hai. Ye aapka Final Complete Code hai.

# Ismein Login, reCAPTCHA, Admin Security, aur AI Semantic Search sab kuch shamil hai.



import os 
import json
import requests
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from supabase import create_client, Client 

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration & Security Settings ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")
LOGIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "login.html")

# Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "ZT_Password_123"
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# Supabase Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Helper: Authentication Check ---
def is_authenticated(request: Request):
    user_session = request.cookies.get("admin_session")
    if user_session != "active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return True

# --- Auth Routes ---

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    if os.path.exists(LOGIN_HTML_PATH):
        with open(LOGIN_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: login.html not found!</h1>"

@app.post("/login")
async def do_login(
    username: str = Form(...), 
    password: str = Form(...), 
    g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")
):
    # 1. Verify reCAPTCHA
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    res = requests.post(verify_url, data={
        "secret": RECAPTCHA_SECRET_KEY,
        "response": g_recaptcha_response
    }).json()

    if not res.get("success"):
        return HTMLResponse("<h2>Captcha Verification Failed! Please try again.</h2>", status_code=400)

    # 2. Check Credentials
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin-zt", status_code=303)
        response.set_cookie(key="admin_session", value="active", httponly=True, max_age=86400) # 24 Hours
        return response
    
    return HTMLResponse("<h2>Invalid Username or Password!</h2>", status_code=401)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("admin_session")
    return response

# --- Protected UI & API Routes ---

@app.get("/", response_class=HTMLResponse)
async def get_home():
    if os.path.exists(HTML_PATH):
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: index.html not found!</h1>"

@app.get("/admin-zt", response_class=HTMLResponse)
async def get_admin(request: Request):
    try:
        is_authenticated(request)
        if os.path.exists(ADMIN_HTML_PATH):
            with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
                return f.read()
    except:
        return RedirectResponse(url="/login")
    return "<h1>Error: admin.html not found!</h1>"

@app.post("/add-faq")
async def add_faq(request: Request):
    try:
        is_authenticated(request)
        data = await request.json()
        q = data.get("question").strip().lower()
        a = data.get("answer").strip()
        supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
        return {"status": "success"}
    except:
        return {"status": "error", "message": "Unauthorized"}

@app.get("/get-faqs")
async def get_faqs(request: Request):
    try:
        is_authenticated(request)
        response = supabase.table("manual_faqs").select("*").execute()
        return response.data
    except:
        return []

@app.delete("/delete-faq/{faq_id}")
async def delete_faq(faq_id: int, request: Request):
    try:
        is_authenticated(request)
        supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
        return {"status": "success"}
    except:
        return {"status": "error", "message": "Unauthorized"}

# --- AI Logic (The Semantic Search) ---

def get_context():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return f.read()[:8000]
    return "No hosting info available."

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.3-70b-versatile", 
    temperature=0.1 
)

prompt = ChatPromptTemplate.from_template("""
You are the Official ZT Hosting Support AI.
STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
Context: {context}
User Question: {input}
Answer:""")

@app.post("/ask")
async def ask_bot(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return {"answer": "Please provide a message."}

        # 1. Semantic Match with DB Questions
        db_res = supabase.table("manual_faqs").select("question, answer").execute()
        db_data = db_res.data

        if db_data:
            db_questions = [row['question'] for row in db_data]
            
            verification_prompt = f"""
            User Question: "{user_input}"
            Available FAQs: {db_questions}
            Task: Does the User Question have the same meaning as any of the Available FAQs? 
            - If YES, return ONLY the exact matching question from the list.
            - If NO, return 'NO_MATCH'.
            Return only the text, no explanation.
            """
            
            match_check = llm.invoke(verification_prompt)
            matched_q = match_check.content.strip()

            if "NO_MATCH" not in matched_q:
                for row in db_data:
                    if row['question'].lower() in matched_q.lower():
                        return {"answer": row['answer']}

        # 2. Fallback to AI with File Context
        context = get_context()
        full_prompt = prompt.format(context=context, input=user_input)
        response = llm.invoke(full_prompt)
        
        return {"answer": response.content}
    
    except Exception as e:
        return {"answer": f"System Error: {str(e)}"}