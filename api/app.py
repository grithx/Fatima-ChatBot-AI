# # # # # # # # # # # # # # # # # # # # # # # import streamlit as st
# # # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # # # # # # # Page Configuration
# # # # # # # # # # # # # # # # # # # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # # # # # # # # # # # # # # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # # # # # # # # # # # # # # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # # # # # # # # # # # # # # # # # # Load Environment Variables
# # # # # # # # # # # # # # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # # # # # # # # # # # # # Sidebar for Status
# # # # # # # # # # # # # # # # # # # # # # # with st.sidebar:
# # # # # # # # # # # # # # # # # # # # # # #     st.header("System Status")
# # # # # # # # # # # # # # # # # # # # # # #     if os.path.exists("./db"):
# # # # # # # # # # # # # # # # # # # # # # #         st.success("Database: Connected")
# # # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # # #         st.error("Database: Not Found! Run ingest.py first.")
    
# # # # # # # # # # # # # # # # # # # # # # #     if st.button("Clear Chat History"):
# # # # # # # # # # # # # # # # # # # # # # #         st.session_state.messages = []

# # # # # # # # # # # # # # # # # # # # # # # # Initialize Models (Cached for speed)
# # # # # # # # # # # # # # # # # # # # # # # @st.cache_resource
# # # # # # # # # # # # # # # # # # # # # # # def load_rag_system():
# # # # # # # # # # # # # # # # # # # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # # # # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # # # # # # # # # # # # # # # # # # #     llm = ChatGroq(
# # # # # # # # # # # # # # # # # # # # # # #         groq_api_key=os.getenv("GROQ_API_KEY"),
# # # # # # # # # # # # # # # # # # # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # # # # # # # # # # # # # # # # # # #         temperature=0.2
# # # # # # # # # # # # # # # # # # # # # # #     )
# # # # # # # # # # # # # # # # # # # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # # # # # #     Context: {context}
# # # # # # # # # # # # # # # # # # # # # # #     Question: {input}
# # # # # # # # # # # # # # # # # # # # # # #     Answer:""")
    
# # # # # # # # # # # # # # # # # # # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # # # # # # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # # # # # # # # # # # # # chain = load_rag_system()

# # # # # # # # # # # # # # # # # # # # # # # # Chat History Setup
# # # # # # # # # # # # # # # # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # # # # # # # # # # # # # # # #     st.session_state.messages = []

# # # # # # # # # # # # # # # # # # # # # # # # Display chat messages from history
# # # # # # # # # # # # # # # # # # # # # # # for message in st.session_state.messages:
# # # # # # # # # # # # # # # # # # # # # # #     with st.chat_message(message["role"]):
# # # # # # # # # # # # # # # # # # # # # # #         st.markdown(message["content"])

# # # # # # # # # # # # # # # # # # # # # # # # User Input
# # # # # # # # # # # # # # # # # # # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # # # # # # # # # # # # # # # # # # #     # Add user message to history
# # # # # # # # # # # # # # # # # # # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # # # # # # # # # # # # # # # # # #     with st.chat_message("user"):
# # # # # # # # # # # # # # # # # # # # # # #         st.markdown(prompt)

# # # # # # # # # # # # # # # # # # # # # # #     # Generate Response
# # # # # # # # # # # # # # # # # # # # # # #     with st.chat_message("assistant"):
# # # # # # # # # # # # # # # # # # # # # # #         with st.spinner("Thinking..."):
# # # # # # # # # # # # # # # # # # # # # # #             response = chain.invoke({"input": prompt})
# # # # # # # # # # # # # # # # # # # # # # #             full_response = response["answer"]
# # # # # # # # # # # # # # # # # # # # # # #             st.markdown(full_response)
    
# # # # # # # # # # # # # # # # # # # # # # #     # Add assistant response to history
# # # # # # # # # # # # # # # # # # # # # # #     st.session_state.messages.append({"role": "assistant", "content": full_response})





# # # # # # # # # # # # # # # # # # # # # # # -------------------------------------------------------------------------
# # # # # # # # # # # # # # # # # # # # # # # CRITICAL FIX: This must be the very first code in the file
# # # # # # # # # # # # # # # # # # # # # # # This swaps the system sqlite3 with pysqlite3-binary for ChromaDB support
# # # # # # # # # # # # # # # # # # # # # # # __import__('pysqlite3')
# # # # # # # # # # # # # # # # # # # # # # # import sys
# # # # # # # # # # # # # # # # # # # # # # # sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # # # # # # # # # # # # -------------------------------------------------------------------------

# # # # # # # # # # # # # # # # # # # # # # import streamlit as st
# # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # # # # # # Page Configuration
# # # # # # # # # # # # # # # # # # # # # # st.set_page_config(page_title="ZT Hosting AI Assistant", page_icon="🤖")
# # # # # # # # # # # # # # # # # # # # # # st.title("🌐 ZT Hosting Support Bot")
# # # # # # # # # # # # # # # # # # # # # # st.markdown("Ask anything about our hosting plans and services!")

# # # # # # # # # # # # # # # # # # # # # # # Load Environment Variables (Try .env first, fallback to st.secrets)
# # # # # # # # # # # # # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # # # # # # # # # # # # Securely get API Key
# # # # # # # # # # # # # # # # # # # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # # # # # # # # # # # # # # # # # # if not groq_api_key and "GROQ_API_KEY" in st.secrets:
# # # # # # # # # # # # # # # # # # # # # #     groq_api_key = st.secrets["GROQ_API_KEY"]

# # # # # # # # # # # # # # # # # # # # # # if not groq_api_key:
# # # # # # # # # # # # # # # # # # # # # #     st.error("⚠️ GROQ_API_KEY is missing! Please add it to .env or Streamlit Secrets.")
# # # # # # # # # # # # # # # # # # # # # #     st.stop()

# # # # # # # # # # # # # # # # # # # # # # # Sidebar for Status
# # # # # # # # # # # # # # # # # # # # # # db_path = "./db"
# # # # # # # # # # # # # # # # # # # # # # db_exists = os.path.exists(db_path) and os.listdir(db_path)

# # # # # # # # # # # # # # # # # # # # # # with st.sidebar:
# # # # # # # # # # # # # # # # # # # # # #     st.header("System Status")
# # # # # # # # # # # # # # # # # # # # # #     if db_exists:
# # # # # # # # # # # # # # # # # # # # # #         st.success("Database: Connected")
# # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # #         st.error("Database: Not Found!")
# # # # # # # # # # # # # # # # # # # # # #         st.warning("⚠️ Please run `ingest.py` locally and commit the `db` folder to GitHub.")
    
# # # # # # # # # # # # # # # # # # # # # #     if st.button("Clear Chat History"):
# # # # # # # # # # # # # # # # # # # # # #         st.session_state.messages = []
# # # # # # # # # # # # # # # # # # # # # #         st.rerun()

# # # # # # # # # # # # # # # # # # # # # # # Initialize Models (Cached for speed)
# # # # # # # # # # # # # # # # # # # # # # @st.cache_resource
# # # # # # # # # # # # # # # # # # # # # # def load_rag_system():
# # # # # # # # # # # # # # # # # # # # # #     # Only load if DB exists to avoid crashing
# # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(db_path):
# # # # # # # # # # # # # # # # # # # # # #         return None

# # # # # # # # # # # # # # # # # # # # # #     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
# # # # # # # # # # # # # # # # # # # # # #     # Initialize Chroma
# # # # # # # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    
# # # # # # # # # # # # # # # # # # # # # #     llm = ChatGroq(
# # # # # # # # # # # # # # # # # # # # # #         groq_api_key=groq_api_key,
# # # # # # # # # # # # # # # # # # # # # #         model_name="llama-3.3-70b-versatile",
# # # # # # # # # # # # # # # # # # # # # #         temperature=0.2
# # # # # # # # # # # # # # # # # # # # # #     )
    
# # # # # # # # # # # # # # # # # # # # # #     prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # # # # #     You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # # # # #     Use the following pieces of retrieved context to answer the question. 
# # # # # # # # # # # # # # # # # # # # # #     If you don't know the answer, just say that you don't know. 
    
# # # # # # # # # # # # # # # # # # # # # #     Context: {context}
    
# # # # # # # # # # # # # # # # # # # # # #     Question: {input}
# # # # # # # # # # # # # # # # # # # # # #     Answer:""")
    
# # # # # # # # # # # # # # # # # # # # # #     document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # # # # # # # # #     return create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # # # # # # # # # # # # # Load the chain
# # # # # # # # # # # # # # # # # # # # # # if db_exists:
# # # # # # # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # # # # # # #         chain = load_rag_system()
# # # # # # # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # # # # # # #         st.error(f"Error loading model: {e}")
# # # # # # # # # # # # # # # # # # # # # #         chain = None
# # # # # # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # # # # # #     chain = None

# # # # # # # # # # # # # # # # # # # # # # # Chat History Setup
# # # # # # # # # # # # # # # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # # # # # # # # # # # # # # #     st.session_state.messages = []

# # # # # # # # # # # # # # # # # # # # # # # Display chat messages from history
# # # # # # # # # # # # # # # # # # # # # # for message in st.session_state.messages:
# # # # # # # # # # # # # # # # # # # # # #     with st.chat_message(message["role"]):
# # # # # # # # # # # # # # # # # # # # # #         st.markdown(message["content"])

# # # # # # # # # # # # # # # # # # # # # # # User Input
# # # # # # # # # # # # # # # # # # # # # # if prompt := st.chat_input("How can I help you today?"):
# # # # # # # # # # # # # # # # # # # # # #     # Add user message to history
# # # # # # # # # # # # # # # # # # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # # # # # # # # # # # # # # # # # #     with st.chat_message("user"):
# # # # # # # # # # # # # # # # # # # # # #         st.markdown(prompt)

# # # # # # # # # # # # # # # # # # # # # #     # Check if system is ready
# # # # # # # # # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # # # # # # # # #         st.error("The AI Brain is not loaded. Please ensure the database is generated and uploaded.")
# # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # #         # Generate Response
# # # # # # # # # # # # # # # # # # # # # #         with st.chat_message("assistant"):
# # # # # # # # # # # # # # # # # # # # # #             with st.spinner("Searching knowledge base..."):
# # # # # # # # # # # # # # # # # # # # # #                 try:
# # # # # # # # # # # # # # # # # # # # # #                     response = chain.invoke({"input": prompt})
# # # # # # # # # # # # # # # # # # # # # #                     full_response = response["answer"]
# # # # # # # # # # # # # # # # # # # # # #                     st.markdown(full_response)
                    
# # # # # # # # # # # # # # # # # # # # # #                     # Add assistant response to history
# # # # # # # # # # # # # # # # # # # # # #                     st.session_state.messages.append({"role": "assistant", "content": full_response})
# # # # # # # # # # # # # # # # # # # # # #                 except Exception as e:
# # # # # # # # # # # # # # # # # # # # # #                     st.error(f"An error occurred: {str(e)}")



# # # # # # # # # # # # # # # # # # # # # # node js conversion



# # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # # # # # # # CORS allow karein taake frontend connect ho sake
# # # # # # # # # # # # # # # # # # # # # app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# # # # # # # # # # # # # # # # # # # # # # Load RAG System
# # # # # # # # # # # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# # # # # # # # # # # # # # # # # # # # # vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)
# # # # # # # # # # # # # # # # # # # # # llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile", temperature=0.2)

# # # # # # # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)

# # # # # # # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # # # # # # # # #     response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # # # # # # # # #     return {"answer": response["answer"]}



# # # # # # # # # # # # # # # # # # # # # update the path of the db becuase we have move the app.py into the api folder


# # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # # # # Environment variables load karein
# # # # # # # # # # # # # # # # # # # # load_dotenv()

# # # # # # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # # # # # # CORS settings: Taake aapka frontend backend se asani se baat kar sake
# # # # # # # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # # # # --- Path Correction ---
# # # # # # # # # # # # # # # # # # # # # Chunkay ye file 'api' folder mein hai, humein '../db' use karna hoga 
# # # # # # # # # # # # # # # # # # # # # taake code ek step piche ja kar 'db' folder ko dhund sakay.
# # # # # # # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # # # # # # # # # Load RAG System
# # # # # # # # # # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # # # # # # # # # # # # # Vector Database check aur connection
# # # # # # # # # # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # # # #     print(f"Warning: Database folder not found at {DB_PATH}")
# # # # # # # # # # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # # # Use the provided context to answer the user's question accurately.
# # # # # # # # # # # # # # # # # # # # If you don't know the answer, politely say so.

# # # # # # # # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # # # # # # Chain Setup
# # # # # # # # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # # # # # # # # # # # # # if vector_db:
# # # # # # # # # # # # # # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # # # #     chain = None

# # # # # # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # # # # # # #         return {"answer": "Error: AI database not found. Please check paths."}
        
# # # # # # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # # # # # #     user_input = data.get("message")
    
# # # # # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # # # # #         return {"answer": f"Sorry, an error occurred: {str(e)}"}




# # # # # # # # # # # # # # # # # # # # update the code to fix the crash isssue of chatbot


# # # # # # # # # # # # # # # # # # # # --- SQLite Fix (Deployment ke liye zaroori) ---
# # # # # # # # # # # # # # # # # # # try:
# # # # # # # # # # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # # # # # # # # # #     import sys
# # # # # # # # # # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # # # # # # # # except ImportError:
# # # # # # # # # # # # # # # # # # #     pass 

# # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # # # from langchain_huggingface import HuggingFaceEmbeddings
# # # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # # # --- Path Handling ---
# # # # # # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # # # # # # # # Load Models
# # # # # # # # # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # # # # # # # # # # # # Database Connect
# # # # # # # # # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # # # # # # # # # # # # if vector_db:
# # # # # # # # # # # # # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # # #     chain = None

# # # # # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # # # # # #         return {"answer": "Error: Database folder not found. Please ensure 'db' folder is uploaded."}
    
# # # # # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # # # # #     user_input = data.get("message")
    
# # # # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}


# # # # # # # # # # # # # # # # # # # Vercel par 250 MB ki limit exceed hone ki sab se bari wajah langchain-huggingface library hai, kyunke ye apne saath PyTorch aur heavy models download karti hai. Isay bypass karne ke liye humein "Lightweight" approach apnaani hogi.

# # # # # # # # # # # # # # # # # # # Niche diya gaya code aapke api/app.py ko optimize kar dega taake size kam ho jaye:




# # # # # # # # # # # # # # # # # # try:
# # # # # # # # # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # # # # # # # # #     import sys
# # # # # # # # # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # # # # # # # except ImportError:
# # # # # # # # # # # # # # # # # #     pass 

# # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # # # from dotenv import load_dotenv

# # # # # # # # # # # # # # # # # # # Lightweight Embeddings and Components
# # # # # # # # # # # # # # # # # # from langchain_community.embeddings import HealthcareHuggingFaceEmbeddings # Ya niche wala alternative
# # # # # # # # # # # # # # # # # # from langchain_community.embeddings import HuggingFaceEmbeddings 
# # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # # --- Path Handling ---
# # # # # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # # # # # # # Load Models - optimized for size
# # # # # # # # # # # # # # # # # # # Note: all-MiniLM-L6-v2 is small, but the library matters
# # # # # # # # # # # # # # # # # # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # # # # # # # # # # # # # # # # # # Database Connect
# # # # # # # # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)

# # # # # # # # # # # # # # # # # # if vector_db:
# # # # # # # # # # # # # # # # # #     chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)
# # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # #     chain = None

# # # # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # # # # #         return {"answer": "Error: Database folder not found."}
    
# # # # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # # # #     user_input = data.get("message")
    
# # # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # # # # # # # # # # # try:
# # # # # # # # # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # # # # # # # # #     import sys
# # # # # # # # # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # # # # # # # except ImportError:
# # # # # # # # # # # # # # # # # #     pass 

# # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # # from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# # # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # # # # # # # Memory-efficient embeddings
# # # # # # # # # # # # # # # # # # embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# # # # # # # # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# # # # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # # # # #         return {"answer": "Error: Database folder not found."}
# # # # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # # # # # # # # # # try:
# # # # # # # # # # # # # # # # #     __import__('pysqlite3')
# # # # # # # # # # # # # # # # #     import sys
# # # # # # # # # # # # # # # # #     sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# # # # # # # # # # # # # # # # # except ImportError:
# # # # # # # # # # # # # # # # #     pass 

# # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # # from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# # # # # # # # # # # # # # # # # from langchain_chroma import Chroma
# # # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # # # # # # from langchain.chains.combine_documents import create_stuff_documents_chain
# # # # # # # # # # # # # # # # # from langchain.chains import create_retrieval_chain

# # # # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # # Path Handling
# # # # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # # # DB_PATH = os.path.join(BASE_DIR, "db")

# # # # # # # # # # # # # # # # # # Wahi embeddings jo database banate waqt use kiye
# # # # # # # # # # # # # # # # # embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# # # # # # # # # # # # # # # # # if os.path.exists(DB_PATH):
# # # # # # # # # # # # # # # # #     vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
# # # # # # # # # # # # # # # # # else:
# # # # # # # # # # # # # # # # #     vector_db = None

# # # # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # # Context: {context}
# # # # # # # # # # # # # # # # # Question: {input}
# # # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # # document_chain = create_stuff_documents_chain(llm, prompt)
# # # # # # # # # # # # # # # # # chain = create_retrieval_chain(vector_db.as_retriever(), document_chain) if vector_db else None

# # # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # # #     if not chain:
# # # # # # # # # # # # # # # # #         return {"answer": "Error: Database folder not found."}
# # # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # #         response = chain.invoke({"input": user_input})
# # # # # # # # # # # # # # # # #         return {"answer": response["answer"]}
# # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}
    


# # # # # # # # # # # # # # # # # ye code bina kisi local embedding model ke chahay ga. Ye seedha text file (zt_data.txt) ko read karega aur Groq ko bhej dega. Ye 100% 250MB se kam hoga.


# # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # # Knowledge Base Read Karein
# # # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")

# # # # # # # # # # # # # # # # def get_context():
# # # # # # # # # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # # # # # #             return f.read()[:10000] # Pehle 10k characters (Vercel limits ke liye)
# # # # # # # # # # # # # # # #     return "No hosting info available."

# # # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # # Use the following context to answer:
# # # # # # # # # # # # # # # # {context}

# # # # # # # # # # # # # # # # User Question: {input}
# # # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # # # #     context = get_context()
    
# # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # # # # # # # # #         response = llm.invoke(full_prompt)
# # # # # # # # # # # # # # # #         return {"answer": response.content}
# # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse # Naya import
# # # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html") # HTML ka path

# # # # # # # # # # # # # # # # --- Naya Route: Chatbot ka Page dikhane ke liye ---
# # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # async def get_index():
# # # # # # # # # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # # # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # # # # #             return f.read()
# # # # # # # # # # # # # # #     return "<h1>Index.html not found in templates/</h1>"

# # # # # # # # # # # # # # # def get_context():
# # # # # # # # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # # # # #             return f.read()[:10000]
# # # # # # # # # # # # # # #     return "No hosting info available."

# # # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # # Use the following context to answer:
# # # # # # # # # # # # # # # {context}

# # # # # # # # # # # # # # # User Question: {input}
# # # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # # #     context = get_context()
# # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # # # # # # # #         response = llm.invoke(full_prompt)
# # # # # # # # # # # # # # #         return {"answer": response.content}
# # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}



# # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # # # )

# # # # # # # # # # # # # # # Path settings
# # # # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # # # # # # # # Aapki index.html ka sahi path
# # # # # # # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# # # # # # # # # # # # # # # 🏠 Home Route: Ye aapka interface dikhayega
# # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # async def get_home():
# # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # #         if os.path.exists(HTML_PATH):
# # # # # # # # # # # # # #             with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # # # #                 return f.read()
# # # # # # # # # # # # # #         return "<h1>Error: templates/index.html not found!</h1>"
# # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # #         return f"<h1>Internal Error: {str(e)}</h1>"

# # # # # # # # # # # # # # # 🤖 AI Logic
# # # # # # # # # # # # # # def get_context():
# # # # # # # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # # # #             return f.read()[:10000]
# # # # # # # # # # # # # #     return "No hosting info available."

# # # # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # # # #     temperature=0.2
# # # # # # # # # # # # # # )

# # # # # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # # # # You are a professional customer support assistant for ZT Hosting. 
# # # # # # # # # # # # # # Use the following context to answer the user:
# # # # # # # # # # # # # # {context}

# # # # # # # # # # # # # # User Question: {input}
# # # # # # # # # # # # # # Answer:""")

# # # # # # # # # # # # # # # 💬 API Route: Ye chat ka jawab dega
# # # # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # # # #     user_input = data.get("message")
# # # # # # # # # # # # # #     context = get_context()
# # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # # # # # # #         response = llm.invoke(full_prompt)
# # # # # # # # # # # # # #         return {"answer": response.content}
# # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # #         return {"answer": f"AI Error: {str(e)}"}


# # # # # # # # # # # # # # update code to give the Bilkul, ye raha aapka complete updated api/app.py. Maine is mein aapka naya professional prompt, temperature settings, aur file paths ko organize kar diya hai taake bot bilkul to-the-point jawab de.



# # # # # # # # # # # import os
# # # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate

# # # # # # # # # # # load_dotenv()
# # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # app.add_middleware(
# # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # )

# # # # # # # # # # # # --- Path Settings ---
# # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")

# # # # # # # # # # # # --- UI Route ---
# # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # async def get_home():
# # # # # # # # # # #     try:
# # # # # # # # # # #         if os.path.exists(HTML_PATH):
# # # # # # # # # # #             with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # #                 return f.read()
# # # # # # # # # # #         return "<h1>Error: templates/index.html not found!</h1>"
# # # # # # # # # # #     except Exception as e:
# # # # # # # # # # #         return f"<h1>Internal Error: {str(e)}</h1>"

# # # # # # # # # # # # --- AI Logic & Professional Prompting ---
# # # # # # # # # # # def get_context():
# # # # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # #             # Context window limit to avoid token overflow
# # # # # # # # # # #             return f.read()[:8000]
# # # # # # # # # # #     return "No hosting info available."

# # # # # # # # # # # # Low temperature (0.1) keeps the bot factual and avoids 'hallucinations'
# # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # #     temperature=0.1 
# # # # # # # # # # # )

# # # # # # # # # # # # Professional & Structured Prompt
# # # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # # You are the Official ZT Hosting Support AI. Your goal is to provide concise, professional, and structured information.

# # # # # # # # # # # STRICT GUIDELINES:
# # # # # # # # # # # 1. ONLY use information from the provided context. If not found, say you don't know politely.
# # # # # # # # # # # 2. BE CONCISE: Answer directly. No "Hello", "I hope you're well", or long intros. 
# # # # # # # # # # # 3. FORMATTING: Use **bold** for prices and plan names. Use bullet points for features.
# # # # # # # # # # # 4. STRUCTURE: Responses must be highly organized. Use tables for plan comparisons.
# # # # # # # # # # # 5. NO EXTRA INFO: Do not suggest other plans unless requested.
# # # # # # # # # # # 6. LANGUAGE: If the question is in Roman Urdu, respond in Roman Urdu with this same professional structure.

# # # # # # # # # # # Context:
# # # # # # # # # # # {context}

# # # # # # # # # # # User Question: {input}
# # # # # # # # # # # Answer:""")

# # # # # # # # # # # # --- Chat API Route ---
# # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # #     try:
# # # # # # # # # # #         data = await request.json()
# # # # # # # # # # #         user_input = data.get("message")
        
# # # # # # # # # # #         if not user_input:
# # # # # # # # # # #             return {"answer": "Please provide a message."}

# # # # # # # # # # #         context = get_context()
        
# # # # # # # # # # #         # Generating structured response
# # # # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # # # #         response = llm.invoke(full_prompt)
        
# # # # # # # # # # #         return {"answer": response.content}
    
# # # # # # # # # # #     except Exception as e:
# # # # # # # # # # #         return {"answer": f"System Error: {str(e)}"}



# # # # # # # # # # # # # Aapki app.py FastAPI use kar rahi hai, jo ke bohat achi baat hai kyunki ye Flask se fast hai. Ab hum isi file mein Admin Side logic aur Supabase Vector Search ko integrate karenge.



# # # # # # # # # # # # import os
# # # # # # # # # # # # import requests
# # # # # # # # # # # # from fastapi import FastAPI, Request, Depends, HTTPException
# # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # # # # # from fastapi.security import HTTPBasic, HTTPBasicCredentials
# # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # from supabase import create_client

# # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # security = HTTPBasic()

# # # # # # # # # # # # # --- Security: Admin Authentication ---
# # # # # # # # # # # # def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
# # # # # # # # # # # #     correct_username = "admin"
# # # # # # # # # # # #     correct_password = "eagale123" # Sir ke liye password
# # # # # # # # # # # #     if credentials.username != correct_username or credentials.password != correct_password:
# # # # # # # # # # # #         raise HTTPException(status_code=401, detail="Invalid Credentials")
# # # # # # # # # # # #     return credentials.username

# # # # # # # # # # # # # --- Middleware & Database ---
# # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # )

# # # # # # # # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # # # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # # # # # # # supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # # # # # # # # --- Path Settings ---
# # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # # # # # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # # # # # # # # # # # --- Helpers: Vector Generation ---
# # # # # # # # # # # # def get_embedding(text):
# # # # # # # # # # # #     # HuggingFace API use kar ke text ko numbers (vectors) mein badalna
# # # # # # # # # # # #     api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
# # # # # # # # # # # #     headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
# # # # # # # # # # # #     response = requests.post(api_url, headers=headers, json={"inputs": text})
# # # # # # # # # # # #     return response.json()

# # # # # # # # # # # # # --- UI Routes ---
# # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # async def get_home():
# # # # # # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # #             return f.read()
# # # # # # # # # # # #     return "<h1>Error: templates/index.html not found!</h1>"

# # # # # # # # # # # # @app.get("/eagale-admin-secret", response_class=HTMLResponse)
# # # # # # # # # # # # async def get_admin(username: str = Depends(authenticate)):
# # # # # # # # # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # # # # # # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # #             return f.read()
# # # # # # # # # # # #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # # # # # # # # # # # --- Admin API: Data Save to DB ---
# # # # # # # # # # # # @app.post("/admin/add-to-db")
# # # # # # # # # # # # async def save_to_db(request: Request, username: str = Depends(authenticate)):
# # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # #     q, a = data.get("question"), data.get("answer")
# # # # # # # # # # # #     vector = get_embedding(q)
    
# # # # # # # # # # # #     supabase.table("bot_knowledge").insert({
# # # # # # # # # # # #         "question": q, 
# # # # # # # # # # # #         "answer": a, 
# # # # # # # # # # # #         "embedding": vector
# # # # # # # # # # # #     }).execute()
    
# # # # # # # # # # # #     return {"message": "Success! Database updated."}

# # # # # # # # # # # # # --- AI Logic & Chat API ---
# # # # # # # # # # # # llm = ChatGroq(
# # # # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # # # #     temperature=0.1 
# # # # # # # # # # # # )

# # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # #     try:
# # # # # # # # # # # #         data = await request.json()
# # # # # # # # # # # #         user_input = data.get("message")
        
# # # # # # # # # # # #         # 1. First, check Supabase for Semantic Match
# # # # # # # # # # # #         query_vector = get_embedding(user_input)
# # # # # # # # # # # #         rpc_res = supabase.rpc("match_knowledge", {
# # # # # # # # # # # #             "query_embedding": query_vector,
# # # # # # # # # # # #             "match_threshold": 0.8,
# # # # # # # # # # # #             "match_count": 1
# # # # # # # # # # # #         }).execute()

# # # # # # # # # # # #         if rpc_res.data:
# # # # # # # # # # # #             return {"answer": rpc_res.data[0]['answer']}
        
# # # # # # # # # # # #         # 2. If not in DB, fallback to text file + Groq
# # # # # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # #             context = f.read()[:8000]
            
# # # # # # # # # # # #         prompt = ChatPromptTemplate.from_template("Context: {context}\n\nUser: {input}\nAnswer:")
# # # # # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # # # # #         response = llm.invoke(full_prompt)
        
# # # # # # # # # # # #         return {"answer": response.content}
# # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # #         return {"answer": f"System Error: {str(e)}"}


# # # # # # # # # # # # add safety check for not crashing the chatbot

# # # # # # # # # # # # import os
# # # # # # # # # # # # import requests
# # # # # # # # # # # # from fastapi import FastAPI, Request, Depends, HTTPException
# # # # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # # # # # from fastapi.security import HTTPBasic, HTTPBasicCredentials
# # # # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # # # from supabase import create_client

# # # # # # # # # # # # load_dotenv()
# # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # security = HTTPBasic()

# # # # # # # # # # # # # --- Security: Admin Authentication ---
# # # # # # # # # # # # def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
# # # # # # # # # # # #     if credentials.username != "admin" or credentials.password != "eagale123":
# # # # # # # # # # # #         raise HTTPException(status_code=401, detail="Invalid Credentials")
# # # # # # # # # # # #     return credentials.username

# # # # # # # # # # # # app.add_middleware(
# # # # # # # # # # # #     CORSMiddleware,
# # # # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # # # #     allow_credentials=True,
# # # # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # # # )

# # # # # # # # # # # # # Initialize Supabase Safely
# # # # # # # # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # # # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # # # # # # # supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# # # # # # # # # # # # # Path Settings
# # # # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # # # # # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")
# # # # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")

# # # # # # # # # # # # def get_embedding(text):
# # # # # # # # # # # #     try:
# # # # # # # # # # # #         api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
# # # # # # # # # # # #         headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
# # # # # # # # # # # #         response = requests.post(api_url, headers=headers, json={"inputs": text}, timeout=10)
# # # # # # # # # # # #         res_data = response.json()
# # # # # # # # # # # #         if isinstance(res_data, list):
# # # # # # # # # # # #             return res_data
# # # # # # # # # # # #         return [0] * 384 # Fallback vector if HF fails
# # # # # # # # # # # #     except:
# # # # # # # # # # # #         return [0] * 384

# # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # async def get_home():
# # # # # # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # #             return f.read()
# # # # # # # # # # # #     return "<h1>Templates folder not found!</h1>"

# # # # # # # # # # # # @app.get("/eagale-admin-secret", response_class=HTMLResponse)
# # # # # # # # # # # # async def get_admin(username: str = Depends(authenticate)):
# # # # # # # # # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # # # # # # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # #             return f.read()
# # # # # # # # # # # #     return "<h1>Admin Template not found!</h1>"

# # # # # # # # # # # # @app.post("/admin/add-to-db")
# # # # # # # # # # # # async def save_to_db(request: Request, username: str = Depends(authenticate)):
# # # # # # # # # # # #     data = await request.json()
# # # # # # # # # # # #     q, a = data.get("question"), data.get("answer")
# # # # # # # # # # # #     vector = get_embedding(q)
# # # # # # # # # # # #     if supabase:
# # # # # # # # # # # #         supabase.table("bot_knowledge").insert({"question": q, "answer": a, "embedding": vector}).execute()
# # # # # # # # # # # #     return {"message": "Database updated."}

# # # # # # # # # # # # @app.post("/ask")
# # # # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # # # #     try:
# # # # # # # # # # # #         data = await request.json()
# # # # # # # # # # # #         user_input = data.get("message")
        
# # # # # # # # # # # #         # Semantic Search with Supabase
# # # # # # # # # # # #         if supabase:
# # # # # # # # # # # #             query_vector = get_embedding(user_input)
# # # # # # # # # # # #             rpc_res = supabase.rpc("match_knowledge", {
# # # # # # # # # # # #                 "query_embedding": query_vector,
# # # # # # # # # # # #                 "match_threshold": 0.8,
# # # # # # # # # # # #                 "match_count": 1
# # # # # # # # # # # #             }).execute()
# # # # # # # # # # # #             if rpc_res.data:
# # # # # # # # # # # #                 return {"answer": rpc_res.data[0]['answer']}

# # # # # # # # # # # #         # Fallback to Text File
# # # # # # # # # # # #         context = ""
# # # # # # # # # # # #         if os.path.exists(DATA_PATH):
# # # # # # # # # # # #             with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # # # #                 context = f.read()[:8000]

# # # # # # # # # # # #         llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile", temperature=0.1)
# # # # # # # # # # # #         prompt = ChatPromptTemplate.from_template("Context: {context}\n\nUser: {input}\nAnswer:")
# # # # # # # # # # # #         response = llm.invoke(prompt.format(context=context, input=user_input))
# # # # # # # # # # # #         return {"answer": response.content}
# # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # #         return {"answer": f"Error: {str(e)}"}



# # # # # # # # # # # update code to add the admin path admin website ka path add kea ha 
# # # # # # # # # # import os 
# # # # # # # # # # import json
# # # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # # from supabase import create_client, Client # Naya import

# # # # # # # # # # load_dotenv()
# # # # # # # # # # app = FastAPI()

# # # # # # # # # # app.add_middleware(
# # # # # # # # # #     CORSMiddleware,
# # # # # # # # # #     allow_origins=["*"],
# # # # # # # # # #     allow_credentials=True,
# # # # # # # # # #     allow_methods=["*"],
# # # # # # # # # #     allow_headers=["*"],
# # # # # # # # # # )

# # # # # # # # # # # --- Path Settings ---
# # # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # # # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # # # # # # # # # --- Supabase Setup ---
# # # # # # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # # # # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # # # # # # --- UI Routes ---
# # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # async def get_home():
# # # # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # #             return f.read()
# # # # # # # # # #     return "<h1>Error: templates/index.html not found!</h1>"

# # # # # # # # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # # # # # # # async def get_admin():
# # # # # # # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # # # # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # #             return f.read()
# # # # # # # # # #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # # # # # # # # # --- Admin API: Save to Supabase ---
# # # # # # # # # # @app.post("/add-faq")
# # # # # # # # # # async def add_faq(request: Request):
# # # # # # # # # #     try:
# # # # # # # # # #         data = await request.json()
# # # # # # # # # #         q = data.get("question").strip().lower()
# # # # # # # # # #         a = data.get("answer").strip()
        
# # # # # # # # # #         # Supabase mein insert
# # # # # # # # # #         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # # # # # # # # #         return {"status": "success"}
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         return {"status": "error", "message": str(e)}

# # # # # # # # # # # --- AI Logic ---
# # # # # # # # # # def get_context():
# # # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # # #             return f.read()[:8000]
# # # # # # # # # #     return "No hosting info available."

# # # # # # # # # # llm = ChatGroq(
# # # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # # #     temperature=0.1 
# # # # # # # # # # )

# # # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # # You are the Official ZT Hosting Support AI.
# # # # # # # # # # STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# # # # # # # # # # Context: {context}
# # # # # # # # # # User Question: {input}
# # # # # # # # # # Answer:""")

# # # # # # # # # # # --- Chat API Route (Priority: DB -> File/AI) ---
# # # # # # # # # # @app.post("/ask")
# # # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # # #     try:
# # # # # # # # # #         data = await request.json()
# # # # # # # # # #         user_input = data.get("message", "").strip().lower()
        
# # # # # # # # # #         if not user_input:
# # # # # # # # # #             return {"answer": "Please provide a message."}

# # # # # # # # # #         # STEP 1: Check Supabase Database first
# # # # # # # # # #         db_query = supabase.table("manual_faqs").select("answer").eq("question", user_input).execute()
        
# # # # # # # # # #         if db_query.data:
# # # # # # # # # #             # Agar exact match mil gaya to AI ke paas nahi jayenge
# # # # # # # # # #             return {"answer": db_query.data[0]['answer']}

# # # # # # # # # #         # STEP 2: Fallback to AI + Website Context
# # # # # # # # # #         context = get_context()
# # # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # # #         response = llm.invoke(full_prompt)
        
# # # # # # # # # #         return {"answer": response.content}
    
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         return {"answer": f"System Error: {str(e)}"}




# # # # # # # # # # Bilkul, aapka current code bilkul sahi track par hai. Main is mein sirf Smart Search (Semantic matching) aur Delete functionality add kar raha hoon taake bot behtar kaam kare aur Admin Panel professional ho jaye.

# # # # # # # # # # Aapka existing logic (Priority: DB -> AI) bilkul mehfooz hai.



# # # # # # # # # import os 
# # # # # # # # # import json
# # # # # # # # # from fastapi import FastAPI, Request
# # # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # # from dotenv import load_dotenv
# # # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # # from supabase import create_client, Client 

# # # # # # # # # load_dotenv()
# # # # # # # # # app = FastAPI()

# # # # # # # # # app.add_middleware(
# # # # # # # # #     CORSMiddleware,
# # # # # # # # #     allow_origins=["*"],
# # # # # # # # #     allow_credentials=True,
# # # # # # # # #     allow_methods=["*"],
# # # # # # # # #     allow_headers=["*"],
# # # # # # # # # )

# # # # # # # # # # --- Path Settings ---
# # # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # # # # # # # # --- Supabase Setup ---
# # # # # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # # # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # # # # # --- UI Routes ---
# # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # async def get_home():
# # # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # #             return f.read()
# # # # # # # # #     return "<h1>Error: templates/index.html not found!</h1>"

# # # # # # # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # # # # # # async def get_admin():
# # # # # # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # # # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # # #             return f.read()
# # # # # # # # #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # # # # # # # # --- Admin API: Save, Get, and Delete ---
# # # # # # # # # @app.post("/add-faq")
# # # # # # # # # async def add_faq(request: Request):
# # # # # # # # #     try:
# # # # # # # # #         data = await request.json()
# # # # # # # # #         q = data.get("question").strip().lower()
# # # # # # # # #         a = data.get("answer").strip()
# # # # # # # # #         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # # # # # # # #         return {"status": "success"}
# # # # # # # # #     except Exception as e:
# # # # # # # # #         return {"status": "error", "message": str(e)}

# # # # # # # # # @app.get("/get-faqs")
# # # # # # # # # async def get_faqs():
# # # # # # # # #     # Admin panel par list dikhane ke liye
# # # # # # # # #     response = supabase.table("manual_faqs").select("*").execute()
# # # # # # # # #     return response.data

# # # # # # # # # @app.delete("/delete-faq/{faq_id}")
# # # # # # # # # async def delete_faq(faq_id: int):
# # # # # # # # #     try:
# # # # # # # # #         supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
# # # # # # # # #         return {"status": "success"}
# # # # # # # # #     except Exception as e:
# # # # # # # # #         return {"status": "error", "message": str(e)}

# # # # # # # # # # --- AI Logic ---
# # # # # # # # # def get_context():
# # # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # # #             return f.read()[:8000]
# # # # # # # # #     return "No hosting info available."

# # # # # # # # # llm = ChatGroq(
# # # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # # #     temperature=0.1 
# # # # # # # # # )

# # # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # # You are the Official ZT Hosting Support AI.
# # # # # # # # # STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# # # # # # # # # Context: {context}
# # # # # # # # # User Question: {input}
# # # # # # # # # Answer:""")

# # # # # # # # # @app.post("/ask")
# # # # # # # # # async def ask_bot(request: Request):
# # # # # # # # #     try:
# # # # # # # # #         data = await request.json()
# # # # # # # # #         user_input = data.get("message", "").strip()
        
# # # # # # # # #         if not user_input:
# # # # # # # # #             return {"answer": "Please provide a message."}

# # # # # # # # #         # 1. DB se saare sawal mangwao
# # # # # # # # #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # # # # # # #         db_data = db_res.data

# # # # # # # # #         if db_data:
# # # # # # # # #             # DB ke saare sawalon ki list banao
# # # # # # # # #             db_questions = [row['question'] for row in db_data]
            
# # # # # # # # #             # AI se pucho ke kya user ka sawal DB mein mojud kisi sawal se milta hai
# # # # # # # # #             verification_prompt = f"""
# # # # # # # # #             User Question: "{user_input}"
# # # # # # # # #             Available FAQs: {db_questions}
            
# # # # # # # # #             Task: Does the User Question have the same meaning as any of the Available FAQs? 
# # # # # # # # #             - If YES, return ONLY the exact matching question from the list.
# # # # # # # # #             - If NO, return 'NO_MATCH'.
# # # # # # # # #             Return only the text, no explanation.
# # # # # # # # #             """
            
# # # # # # # # #             match_check = llm.invoke(verification_prompt)
# # # # # # # # #             matched_q = match_check.content.strip()

# # # # # # # # #             # Agar AI ko koi milta julta sawal mil gaya
# # # # # # # # #             if "NO_MATCH" not in matched_q:
# # # # # # # # #                 for row in db_data:
# # # # # # # # #                     if row['question'].lower() in matched_q.lower():
# # # # # # # # #                         return {"answer": row['answer']}

# # # # # # # # #         # 2. Agar DB mein match nahi mila, to normal AI + File process
# # # # # # # # #         context = get_context()
# # # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # # #         response = llm.invoke(full_prompt)
        
# # # # # # # # #         return {"answer": response.content}
    
# # # # # # # # #     except Exception as e:
# # # # # # # # #         return {"answer": f"System Error: {str(e)}"}



# # # # # # # # # Bilkul, main aapke existing logic ko bilkul nahi cheron ga. Bas ooper security functions add karoon ga aur aapke Admin routes mein Depends(authenticate) laga doon ga taake ye secure ho jayein.

# # # # # # # # # Ye raha aapka updated code:


# # # # # # # # import os 
# # # # # # # # import json
# # # # # # # # import secrets # New for security
# # # # # # # # from fastapi import FastAPI, Request, Depends, HTTPException, status # Added dependencies
# # # # # # # # from fastapi.security import HTTPBasic, HTTPBasicCredentials # Added for security
# # # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # # from fastapi.responses import HTMLResponse
# # # # # # # # from dotenv import load_dotenv
# # # # # # # # from langchain_groq import ChatGroq
# # # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # # from supabase import create_client, Client 

# # # # # # # # load_dotenv()
# # # # # # # # app = FastAPI()

# # # # # # # # app.add_middleware(
# # # # # # # #     CORSMiddleware,
# # # # # # # #     allow_origins=["*"],
# # # # # # # #     allow_credentials=True,
# # # # # # # #     allow_methods=["*"],
# # # # # # # #     allow_headers=["*"],
# # # # # # # # )

# # # # # # # # # --- Security Settings ---
# # # # # # # # security = HTTPBasic()
# # # # # # # # ADMIN_USERNAME = "admin"
# # # # # # # # ADMIN_PASSWORD = "ZT_Password_123" # <--- Isay aap change kar sakte hain

# # # # # # # # def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
# # # # # # # #     is_username_correct = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
# # # # # # # #     is_password_correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
# # # # # # # #     if not (is_username_correct and is_password_correct):
# # # # # # # #         raise HTTPException(
# # # # # # # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # # # # # # #             detail="Incorrect username or password",
# # # # # # # #             headers={"WWW-Authenticate": "Basic"},
# # # # # # # #         )
# # # # # # # #     return credentials.username

# # # # # # # # # --- Path Settings ---
# # # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")

# # # # # # # # # --- Supabase Setup ---
# # # # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # # # # --- UI Routes ---
# # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # async def get_home():
# # # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # #             return f.read()
# # # # # # # #     return "<h1>Error: templates/index.html not found!</h1>"

# # # # # # # # # Yahan Depends add kiya gaya hai
# # # # # # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # # # # # async def get_admin(username: str = Depends(authenticate)):
# # # # # # # #     if os.path.exists(ADMIN_HTML_PATH):
# # # # # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # # #             return f.read()
# # # # # # # #     return "<h1>Error: templates/admin.html not found!</h1>"

# # # # # # # # # --- Admin API: Save, Get, and Delete (All Secured) ---
# # # # # # # # @app.post("/add-faq")
# # # # # # # # async def add_faq(request: Request, username: str = Depends(authenticate)):
# # # # # # # #     try:
# # # # # # # #         data = await request.json()
# # # # # # # #         q = data.get("question").strip().lower()
# # # # # # # #         a = data.get("answer").strip()
# # # # # # # #         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # # # # # # #         return {"status": "success"}
# # # # # # # #     except Exception as e:
# # # # # # # #         return {"status": "error", "message": str(e)}

# # # # # # # # @app.get("/get-faqs")
# # # # # # # # async def get_faqs(username: str = Depends(authenticate)):
# # # # # # # #     response = supabase.table("manual_faqs").select("*").execute()
# # # # # # # #     return response.data

# # # # # # # # @app.delete("/delete-faq/{faq_id}")
# # # # # # # # async def delete_faq(faq_id: int, username: str = Depends(authenticate)):
# # # # # # # #     try:
# # # # # # # #         supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
# # # # # # # #         return {"status": "success"}
# # # # # # # #     except Exception as e:
# # # # # # # #         return {"status": "error", "message": str(e)}

# # # # # # # # # --- AI Logic (No Changes Here) ---
# # # # # # # # def get_context():
# # # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # # #             return f.read()[:8000]
# # # # # # # #     return "No hosting info available."

# # # # # # # # llm = ChatGroq(
# # # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # # #     temperature=0.1 
# # # # # # # # )

# # # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # # You are the Official ZT Hosting Support AI.
# # # # # # # # STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# # # # # # # # Context: {context}
# # # # # # # # User Question: {input}
# # # # # # # # Answer:""")

# # # # # # # # @app.post("/ask")
# # # # # # # # async def ask_bot(request: Request):
# # # # # # # #     try:
# # # # # # # #         data = await request.json()
# # # # # # # #         user_input = data.get("message", "").strip()
        
# # # # # # # #         if not user_input:
# # # # # # # #             return {"answer": "Please provide a message."}

# # # # # # # #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # # # # # #         db_data = db_res.data

# # # # # # # #         if db_data:
# # # # # # # #             db_questions = [row['question'] for row in db_data]
            
# # # # # # # #             verification_prompt = f"""
# # # # # # # #             User Question: "{user_input}"
# # # # # # # #             Available FAQs: {db_questions}
            
# # # # # # # #             Task: Does the User Question have the same meaning as any of the Available FAQs? 
# # # # # # # #             - If YES, return ONLY the exact matching question from the list.
# # # # # # # #             - If NO, return 'NO_MATCH'.
# # # # # # # #             Return only the text, no explanation.
# # # # # # # #             """
            
# # # # # # # #             match_check = llm.invoke(verification_prompt)
# # # # # # # #             matched_q = match_check.content.strip()

# # # # # # # #             if "NO_MATCH" not in matched_q:
# # # # # # # #                 for row in db_data:
# # # # # # # #                     if row['question'].lower() in matched_q.lower():
# # # # # # # #                         return {"answer": row['answer']}

# # # # # # # #         context = get_context()
# # # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # # #         response = llm.invoke(full_prompt)
        
# # # # # # # #         return {"answer": response.content}
    
# # # # # # # #     except Exception as e:
# # # # # # # #         return {"answer": f"System Error: {str(e)}"}



# # # # # # # # Bilkul, maine aapka diya hua security code aur aapki purani AI logic (Semantic Search wali) dono ko merge kar diya hai. Ye aapka Final Complete Code hai.

# # # # # # # # Ismein Login, reCAPTCHA, Admin Security, aur AI Semantic Search sab kuch shamil hai.



# # # # # # # import os 
# # # # # # # import json
# # # # # # # import requests
# # # # # # # from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
# # # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # # from fastapi.responses import HTMLResponse, RedirectResponse
# # # # # # # from dotenv import load_dotenv
# # # # # # # from langchain_groq import ChatGroq
# # # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # # from supabase import create_client, Client 

# # # # # # # load_dotenv()
# # # # # # # app = FastAPI()

# # # # # # # app.add_middleware(
# # # # # # #     CORSMiddleware,
# # # # # # #     allow_origins=["*"],
# # # # # # #     allow_credentials=True,
# # # # # # #     allow_methods=["*"],
# # # # # # #     allow_headers=["*"],
# # # # # # # )

# # # # # # # # --- Configuration & Security Settings ---
# # # # # # # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # # # # # DATA_PATH = os.path.join(BASE_DIR, "data", "zt_data.txt")
# # # # # # # HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
# # # # # # # ADMIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "admin.html")
# # # # # # # LOGIN_HTML_PATH = os.path.join(BASE_DIR, "templates", "login.html")

# # # # # # # # Credentials
# # # # # # # ADMIN_USERNAME = "admin"
# # # # # # # ADMIN_PASSWORD = "ZT_Password_123"
# # # # # # # RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# # # # # # # # Supabase Setup
# # # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # # # --- Helper: Authentication Check ---
# # # # # # # def is_authenticated(request: Request):
# # # # # # #     user_session = request.cookies.get("admin_session")
# # # # # # #     if user_session != "active":
# # # # # # #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
# # # # # # #     return True

# # # # # # # # --- Auth Routes ---

# # # # # # # @app.get("/login", response_class=HTMLResponse)
# # # # # # # async def get_login():
# # # # # # #     if os.path.exists(LOGIN_HTML_PATH):
# # # # # # #         with open(LOGIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # #             return f.read()
# # # # # # #     return "<h1>Error: login.html not found!</h1>"

# # # # # # # @app.post("/login")
# # # # # # # async def do_login(
# # # # # # #     username: str = Form(...), 
# # # # # # #     password: str = Form(...), 
# # # # # # #     g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")
# # # # # # # ):
# # # # # # #     # 1. Verify reCAPTCHA
# # # # # # #     verify_url = "https://www.google.com/recaptcha/api/siteverify"
# # # # # # #     res = requests.post(verify_url, data={
# # # # # # #         "secret": RECAPTCHA_SECRET_KEY,
# # # # # # #         "response": g_recaptcha_response
# # # # # # #     }).json()

# # # # # # #     if not res.get("success"):
# # # # # # #         return HTMLResponse("<h2>Captcha Verification Failed! Please try again.</h2>", status_code=400)

# # # # # # #     # 2. Check Credentials
# # # # # # #     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
# # # # # # #         response = RedirectResponse(url="/admin-zt", status_code=303)
# # # # # # #         response.set_cookie(key="admin_session", value="active", httponly=True, max_age=86400) # 24 Hours
# # # # # # #         return response
    
# # # # # # #     return HTMLResponse("<h2>Invalid Username or Password!</h2>", status_code=401)

# # # # # # # @app.get("/logout")
# # # # # # # async def logout():
# # # # # # #     response = RedirectResponse(url="/login")
# # # # # # #     response.delete_cookie("admin_session")
# # # # # # #     return response

# # # # # # # # --- Protected UI & API Routes ---

# # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # async def get_home():
# # # # # # #     if os.path.exists(HTML_PATH):
# # # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # #             return f.read()
# # # # # # #     return "<h1>Error: index.html not found!</h1>"

# # # # # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # # # # async def get_admin(request: Request):
# # # # # # #     try:
# # # # # # #         is_authenticated(request)
# # # # # # #         if os.path.exists(ADMIN_HTML_PATH):
# # # # # # #             with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # # #                 return f.read()
# # # # # # #     except:
# # # # # # #         return RedirectResponse(url="/login")
# # # # # # #     return "<h1>Error: admin.html not found!</h1>"

# # # # # # # @app.post("/add-faq")
# # # # # # # async def add_faq(request: Request):
# # # # # # #     try:
# # # # # # #         is_authenticated(request)
# # # # # # #         data = await request.json()
# # # # # # #         q = data.get("question").strip().lower()
# # # # # # #         a = data.get("answer").strip()
# # # # # # #         supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # # # # # #         return {"status": "success"}
# # # # # # #     except:
# # # # # # #         return {"status": "error", "message": "Unauthorized"}

# # # # # # # @app.get("/get-faqs")
# # # # # # # async def get_faqs(request: Request):
# # # # # # #     try:
# # # # # # #         is_authenticated(request)
# # # # # # #         response = supabase.table("manual_faqs").select("*").execute()
# # # # # # #         return response.data
# # # # # # #     except:
# # # # # # #         return []

# # # # # # # @app.delete("/delete-faq/{faq_id}")
# # # # # # # async def delete_faq(faq_id: int, request: Request):
# # # # # # #     try:
# # # # # # #         is_authenticated(request)
# # # # # # #         supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
# # # # # # #         return {"status": "success"}
# # # # # # #     except:
# # # # # # #         return {"status": "error", "message": "Unauthorized"}

# # # # # # # # --- AI Logic (The Semantic Search) ---

# # # # # # # def get_context():
# # # # # # #     if os.path.exists(DATA_PATH):
# # # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # # #             return f.read()[:8000]
# # # # # # #     return "No hosting info available."

# # # # # # # llm = ChatGroq(
# # # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # # #     temperature=0.1 
# # # # # # # )

# # # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # # You are the Official ZT Hosting Support AI.
# # # # # # # STRICT GUIDELINE: ONLY use the context. If not found, say you don't know.
# # # # # # # Context: {context}
# # # # # # # User Question: {input}
# # # # # # # Answer:""")

# # # # # # # @app.post("/ask")
# # # # # # # async def ask_bot(request: Request):
# # # # # # #     try:
# # # # # # #         data = await request.json()
# # # # # # #         user_input = data.get("message", "").strip()
        
# # # # # # #         if not user_input:
# # # # # # #             return {"answer": "Please provide a message."}

# # # # # # #         # 1. Semantic Match with DB Questions
# # # # # # #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # # # # #         db_data = db_res.data

# # # # # # #         if db_data:
# # # # # # #             db_questions = [row['question'] for row in db_data]
            
# # # # # # #             verification_prompt = f"""
# # # # # # #             User Question: "{user_input}"
# # # # # # #             Available FAQs: {db_questions}
# # # # # # #             Task: Does the User Question have the same meaning as any of the Available FAQs? 
# # # # # # #             - If YES, return ONLY the exact matching question from the list.
# # # # # # #             - If NO, return 'NO_MATCH'.
# # # # # # #             Return only the text, no explanation.
# # # # # # #             """
            
# # # # # # #             match_check = llm.invoke(verification_prompt)
# # # # # # #             matched_q = match_check.content.strip()

# # # # # # #             if "NO_MATCH" not in matched_q:
# # # # # # #                 for row in db_data:
# # # # # # #                     if row['question'].lower() in matched_q.lower():
# # # # # # #                         return {"answer": row['answer']}

# # # # # # #         # 2. Fallback to AI with File Context
# # # # # # #         context = get_context()
# # # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # # #         response = llm.invoke(full_prompt)
        
# # # # # # #         return {"answer": response.content}
    
# # # # # # #     except Exception as e:
# # # # # # #         return {"answer": f"System Error: {str(e)}"}



# # # # # # # Bilkul, ye raha aapka final aur complete code. Is mein se purani popup (Basic Auth) logic bilkul khatam kar di gayi hai. Ab agar koi /admin-zt par jane ki koshish karega to wo seedha aapke Login Page par redirect ho jayega.

# # # # # # # Maine Vercel ke liye Pathlib use kiya hai taake "File Not Found" wala masla bhi hal ho jaye.



# # # # # # import os 
# # # # # # import json
# # # # # # import requests
# # # # # # from pathlib import Path
# # # # # # from fastapi import FastAPI, Request, Form, HTTPException, status
# # # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # # from fastapi.responses import HTMLResponse, RedirectResponse
# # # # # # from dotenv import load_dotenv
# # # # # # from langchain_groq import ChatGroq
# # # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # # from supabase import create_client, Client 

# # # # # # load_dotenv()
# # # # # # app = FastAPI()

# # # # # # app.add_middleware(
# # # # # #     CORSMiddleware,
# # # # # #     allow_origins=["*"],
# # # # # #     allow_credentials=True,
# # # # # #     allow_methods=["*"],
# # # # # #     allow_headers=["*"],
# # # # # # )

# # # # # # # --- Configuration & Path Settings (Vercel Fix) ---
# # # # # # # Ye logic file paths ko har server par sahi rakhti hai
# # # # # # BASE_DIR = Path(__file__).resolve().parent.parent
# # # # # # DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
# # # # # # HTML_PATH = BASE_DIR / "templates" / "index.html"
# # # # # # ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
# # # # # # LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# # # # # # # Credentials
# # # # # # ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
# # # # # # ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
# # # # # # RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# # # # # # # Supabase Setup
# # # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # # --- Helper: Authentication Check ---
# # # # # # def check_auth(request: Request):
# # # # # #     # Sirf check karta hai ke user ke paas active session cookie hai ya nahi
# # # # # #     return request.cookies.get("admin_session") == "active"

# # # # # # # --- Auth Routes ---

# # # # # # @app.get("/login", response_class=HTMLResponse)
# # # # # # async def get_login():
# # # # # #     if LOGIN_HTML_PATH.exists():
# # # # # #         with open(LOGIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # #             return f.read()
# # # # # #     return f"<h1>Error: login.html not found!</h1><p>Path: {LOGIN_HTML_PATH}</p>"

# # # # # # @app.post("/login")
# # # # # # async def do_login(
# # # # # #     username: str = Form(...), 
# # # # # #     password: str = Form(...), 
# # # # # #     g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")
# # # # # # ):
# # # # # #     # 1. Verify reCAPTCHA
# # # # # #     verify_url = "https://www.google.com/recaptcha/api/siteverify"
# # # # # #     res = requests.post(verify_url, data={
# # # # # #         "secret": RECAPTCHA_SECRET_KEY,
# # # # # #         "response": g_recaptcha_response
# # # # # #     }).json()

# # # # # #     if not res.get("success"):
# # # # # #         return HTMLResponse("<h2>Captcha Verification Failed! Please complete the captcha.</h2>", status_code=400)

# # # # # #     # 2. Check Credentials
# # # # # #     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
# # # # # #         response = RedirectResponse(url="/admin-zt", status_code=303)
        
# # # # # #         # --- CHANGES START HERE ---
# # # # # #         # max_age hata diya taake browser band hote hi logout ho jaye
# # # # # #         response.set_cookie(
# # # # # #             key="admin_session", 
# # # # # #             value="active", 
# # # # # #             httponly=True, 
# # # # # #             samesite="lax",
# # # # # #             secure=True 
# # # # # #         )
# # # # # #         # --- CHANGES END HERE ---
        
# # # # # #         return response
    
# # # # # #     return HTMLResponse("<h2>Invalid Username or Password!</h2>", status_code=401)

# # # # # # @app.get("/logout")
# # # # # # async def logout():
# # # # # #     response = RedirectResponse(url="/login")
# # # # # #     response.delete_cookie("admin_session")
# # # # # #     return response

# # # # # # # --- UI & Admin API Routes ---

# # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # async def get_home():
# # # # # #     if HTML_PATH.exists():
# # # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # # #             return f.read()
# # # # # #     return "<h1>Main site index.html missing</h1>"

# # # # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # # # async def get_admin(request: Request):
# # # # # #     # Agar login nahi hai, to redirect to /login (No Popup)
# # # # # #     if not check_auth(request):
# # # # # #         return RedirectResponse(url="/login", status_code=303)

# # # # # #     if ADMIN_HTML_PATH.exists():
# # # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # # #             return f.read()
# # # # # #     return "<h1>Admin page file missing</h1>"

# # # # # # @app.post("/add-faq")
# # # # # # async def add_faq(request: Request):
# # # # # #     if not check_auth(request):
# # # # # #         return {"status": "error", "message": "Unauthorized"}
    
# # # # # #     data = await request.json()
# # # # # #     q = data.get("question").strip().lower()
# # # # # #     a = data.get("answer").strip()
# # # # # #     supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # # # # #     return {"status": "success"}

# # # # # # @app.get("/get-faqs")
# # # # # # async def get_faqs(request: Request):
# # # # # #     if not check_auth(request):
# # # # # #         return []
# # # # # #     response = supabase.table("manual_faqs").select("*").execute()
# # # # # #     return response.data

# # # # # # @app.delete("/delete-faq/{faq_id}")
# # # # # # async def delete_faq(faq_id: int, request: Request):
# # # # # #     if not check_auth(request):
# # # # # #         return {"status": "error", "message": "Unauthorized"}
# # # # # #     supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
# # # # # #     return {"status": "success"}

# # # # # # # --- AI Logic (Semantic Search) ---

# # # # # # def get_context():
# # # # # #     if DATA_PATH.exists():
# # # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # # #             return f.read()[:8000]
# # # # # #     return "No hosting info available."

# # # # # # llm = ChatGroq(
# # # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # # #     model_name="llama-3.3-70b-versatile", 
# # # # # #     temperature=0.1 
# # # # # # )

# # # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # # You are the Official ZT Hosting Support AI.
# # # # # # STRICT GUIDELINE: ONLY use the context provided. If not found, say you don't know.
# # # # # # Context: {context}
# # # # # # User Question: {input}
# # # # # # Answer:""")

# # # # # # @app.post("/ask")
# # # # # # async def ask_bot(request: Request):
# # # # # #     try:
# # # # # #         data = await request.json()
# # # # # #         user_input = data.get("message", "").strip()
        
# # # # # #         if not user_input:
# # # # # #             return {"answer": "Please provide a message."}

# # # # # #         # 1. Semantic Match with DB Questions
# # # # # #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # # # #         db_data = db_res.data

# # # # # #         if db_data:
# # # # # #             db_questions = [row['question'] for row in db_data]
            
# # # # # #             verification_prompt = f"""
# # # # # #             User Question: "{user_input}"
# # # # # #             Available FAQs: {db_questions}
# # # # # #             Task: Does the User Question have the same meaning as any of the Available FAQs? 
# # # # # #             - If YES, return ONLY the exact matching question.
# # # # # #             - If NO, return 'NO_MATCH'.
# # # # # #             """
            
# # # # # #             match_check = llm.invoke(verification_prompt)
# # # # # #             matched_q = match_check.content.strip()

# # # # # #             if "NO_MATCH" not in matched_q:
# # # # # #                 for row in db_data:
# # # # # #                     if row['question'].lower() in matched_q.lower():
# # # # # #                         return {"answer": row['answer']}

# # # # # #         # 2. Fallback to AI
# # # # # #         context = get_context()
# # # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # # #         response = llm.invoke(full_prompt)
        
# # # # # #         return {"answer": response.content}
    
# # # # # #     except Exception as e:
# # # # # #         return {"answer": f"System Error: {str(e)}"}


# # # # # # Bilkul, ye raha aapka final aur complete api/app.py code. Is mein humne saari requirements merge kar di hain:

# # # # # # Strict Guardrails: Bot sirf ZT Hosting ke sawal jawab karega.

# # # # # # Session-Only Cookies: Browser band hote hi logout ho jayega.

# # # # # # No Popups: Authentication sirf aapke login page se hogi.

# # # # # # Security: Credentials .env file se liye jayenge.



# # # # # import os 
# # # # # import json
# # # # # import requests
# # # # # from pathlib import Path
# # # # # from fastapi import FastAPI, Request, Form, HTTPException, status
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from fastapi.responses import HTMLResponse, RedirectResponse
# # # # # from dotenv import load_dotenv
# # # # # from langchain_groq import ChatGroq
# # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # from supabase import create_client, Client 

# # # # # load_dotenv()
# # # # # app = FastAPI()

# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # # --- Configuration & Path Settings ---
# # # # # BASE_DIR = Path(__file__).resolve().parent.parent
# # # # # DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
# # # # # HTML_PATH = BASE_DIR / "templates" / "index.html"
# # # # # ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
# # # # # LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# # # # # # Credentials from Environment Variables
# # # # # ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
# # # # # ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
# # # # # RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# # # # # # Supabase Setup
# # # # # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # # # # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # # # # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # # # # # --- Helper: Authentication Check ---
# # # # # def check_auth(request: Request):
# # # # #     return request.cookies.get("admin_session") == "active"

# # # # # # --- Auth Routes ---

# # # # # @app.get("/login", response_class=HTMLResponse)
# # # # # async def get_login():
# # # # #     if LOGIN_HTML_PATH.exists():
# # # # #         with open(LOGIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return f"<h1>Error: login.html not found!</h1>"

# # # # # @app.post("/login")
# # # # # async def do_login(
# # # # #     username: str = Form(...), 
# # # # #     password: str = Form(...), 
# # # # #     g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")
# # # # # ):
# # # # #     # 1. Verify reCAPTCHA
# # # # #     verify_url = "https://www.google.com/recaptcha/api/siteverify"
# # # # #     res = requests.post(verify_url, data={
# # # # #         "secret": RECAPTCHA_SECRET_KEY,
# # # # #         "response": g_recaptcha_response
# # # # #     }).json()

# # # # #     if not res.get("success"):
# # # # #         return HTMLResponse("<h2>Captcha Verification Failed! Please try again.</h2>", status_code=400)

# # # # #     # 2. Check Credentials
# # # # #     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
# # # # #         response = RedirectResponse(url="/admin-zt", status_code=303)
# # # # #         # Session cookie (No max_age means it expires on browser close)
# # # # #         response.set_cookie(
# # # # #             key="admin_session", 
# # # # #             value="active", 
# # # # #             httponly=True, 
# # # # #             samesite="lax",
# # # # #             secure=True 
# # # # #         )
# # # # #         return response
    
# # # # #     return HTMLResponse("<h2>Invalid Username or Password!</h2>", status_code=401)

# # # # # @app.get("/logout")
# # # # # async def logout():
# # # # #     response = RedirectResponse(url="/login")
# # # # #     response.delete_cookie("admin_session")
# # # # #     return response

# # # # # # --- Protected UI & API Routes ---

# # # # # @app.get("/", response_class=HTMLResponse)
# # # # # async def get_home():
# # # # #     if HTML_PATH.exists():
# # # # #         with open(HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return "<h1>Main index.html missing</h1>"

# # # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # # async def get_admin(request: Request):
# # # # #     if not check_auth(request):
# # # # #         return RedirectResponse(url="/login", status_code=303)

# # # # #     if ADMIN_HTML_PATH.exists():
# # # # #         with open(ADMIN_HTML_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()
# # # # #     return "<h1>Admin page file missing</h1>"

# # # # # @app.post("/add-faq")
# # # # # async def add_faq(request: Request):
# # # # #     if not check_auth(request):
# # # # #         return {"status": "error", "message": "Unauthorized"}
# # # # #     data = await request.json()
# # # # #     q = data.get("question").strip().lower()
# # # # #     a = data.get("answer").strip()
# # # # #     supabase.table("manual_faqs").insert({"question": q, "answer": a}).execute()
# # # # #     return {"status": "success"}

# # # # # @app.get("/get-faqs")
# # # # # async def get_faqs(request: Request):
# # # # #     if not check_auth(request): return []
# # # # #     response = supabase.table("manual_faqs").select("*").execute()
# # # # #     return response.data

# # # # # @app.delete("/delete-faq/{faq_id}")
# # # # # async def delete_faq(faq_id: int, request: Request):
# # # # #     if not check_auth(request):
# # # # #         return {"status": "error", "message": "Unauthorized"}
# # # # #     supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
# # # # #     return {"status": "success"}

# # # # # # --- AI Logic (Strict ZT Hosting Only) ---

# # # # # def get_context():
# # # # #     if DATA_PATH.exists():
# # # # #         with open(DATA_PATH, "r", encoding="utf-8") as f:
# # # # #             return f.read()[:8000]
# # # # #     return "No hosting info available."

# # # # # llm = ChatGroq(
# # # # #     groq_api_key=os.getenv("GROQ_API_KEY"), 
# # # # #     model_name="llama-3.3-70b-versatile", 
# # # # #     temperature=0.1 
# # # # # )

# # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # You are the Official ZT Hosting Support AI.

# # # # # STRICT GUIDELINES:
# # # # # 1. ONLY answer questions related to ZT Hosting.
# # # # # 2. If the user asks anything unrelated (general knowledge, coding, weather, personal, etc.), respond with: "Sorry, I am here to provide information about ZT Hosting only."
# # # # # 3. Use the context to answer. If not found, say you don't know but stay on topic.

# # # # # Context: {context}
# # # # # User Question: {input}
# # # # # Answer:""")

# # # # # @app.post("/ask")
# # # # # async def ask_bot(request: Request):
# # # # #     try:
# # # # #         data = await request.json()
# # # # #         user_input = data.get("message", "").strip()
# # # # #         if not user_input: return {"answer": "Please provide a message."}

# # # # #         # 1. Database Check & Topic Validation
# # # # #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # # #         db_data = db_res.data
# # # # #         if db_data:
# # # # #             db_questions = [row['question'] for row in db_data]
# # # # #             verify_prompt = f"Question: {user_input}\nFAQs: {db_questions}\nIs this about ZT Hosting? If yes and matches FAQ return it, if yes no match return 'NO_MATCH', if unrelated return 'OFF_TOPIC'."
# # # # #             match_res = llm.invoke(verify_prompt).content.strip()
            
# # # # #             if "OFF_TOPIC" in match_res:
# # # # #                 return {"answer": "Sorry, I am here to provide information about ZT Hosting only."}
# # # # #             if "NO_MATCH" not in match_res:
# # # # #                 for row in db_data:
# # # # #                     if row['question'].lower() in match_res.lower():
# # # # #                         return {"answer": row['answer']}

# # # # #         # 2. AI Fallback
# # # # #         context = get_context()
# # # # #         full_prompt = prompt.format(context=context, input=user_input)
# # # # #         response = llm.invoke(full_prompt)
# # # # #         return {"answer": response.content.strip()}
    
# # # # #     except Exception as e:
# # # # #         return {"answer": f"System Error: {str(e)}"}



# # # # # update to fix the grok api key invalid issue 


# # # # # import os 
# # # # # from pathlib import Path
# # # # # from fastapi import FastAPI, Request, Form
# # # # # from fastapi.middleware.cors import CORSMiddleware
# # # # # from fastapi.responses import HTMLResponse, RedirectResponse
# # # # # import requests
# # # # # from langchain_groq import ChatGroq
# # # # # from langchain_core.prompts import ChatPromptTemplate
# # # # # from supabase import create_client, Client 

# # # # # app = FastAPI()

# # # # # app.add_middleware(
# # # # #     CORSMiddleware,
# # # # #     allow_origins=["*"],
# # # # #     allow_credentials=True,
# # # # #     allow_methods=["*"],
# # # # #     allow_headers=["*"],
# # # # # )

# # # # # # --- Vercel Specific Path Configuration ---
# # # # # BASE_DIR = Path(__file__).resolve().parent.parent
# # # # # DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
# # # # # HTML_PATH = BASE_DIR / "templates" / "index.html"

# # # # # # --- Secure Client Initialization ---
# # # # # # Hum variables ko function ke andar check karenge taake code crash na ho
# # # # # def get_supabase():
# # # # #     url = os.environ.get("SUPABASE_URL")
# # # # #     key = os.environ.get("SUPABASE_KEY")
# # # # #     if not url or not key:
# # # # #         return None
# # # # #     return create_client(url, key)

# # # # # def get_llm():
# # # # #     api_key = os.environ.get("GROQ_API_KEY")
# # # # #     if not api_key:
# # # # #         return None
# # # # #     return ChatGroq(
# # # # #         groq_api_key=api_key, 
# # # # #         model_name="llama-3.3-70b-versatile", 
# # # # #         temperature=0.1 
# # # # #     )

# # # # # # --- AI Logic (To-the-point & Highlighted) ---

# # # # # prompt = ChatPromptTemplate.from_template("""
# # # # # You are the Official ZT Hosting Support AI.

# # # # # STRICT RULES:
# # # # # 1. **To-the-point**: Give a very direct answer. No "Hello", "How can I help", or filler text.
# # # # # 2. **Highlighting**: Use **bold text** for prices, storage limits, and plan names.
# # # # # 3. **Guardrail**: If the question is not about ZT Hosting, reply ONLY: "Sorry, I am here to provide information about ZT Hosting only."
# # # # # 4. **Structure**: Keep it to 1-2 sentences maximum.

# # # # # Context: {context}
# # # # # User Question: {input}
# # # # # Answer:""")

# # # # # @app.post("/ask")
# # # # # async def ask_bot(request: Request):
# # # # #     try:
# # # # #         data = await request.json()
# # # # #         user_input = data.get("message", "").strip()
        
# # # # #         llm = get_llm()
# # # # #         supabase = get_supabase()

# # # # #         if not llm:
# # # # #             return {"answer": "Error: GROQ_API_KEY is not set in Vercel settings."}

# # # # #         # 1. Database Priority Check
# # # # #         db_context = ""
# # # # #         if supabase:
# # # # #             db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # # #             if db_res.data:
# # # # #                 for row in db_res.data:
# # # # #                     if row['question'].lower() in user_input.lower():
# # # # #                         db_context = f"Manual Info: {row['answer']}"
# # # # #                         break

# # # # #         # 2. File Context
# # # # #         file_context = ""
# # # # #         if DATA_PATH.exists():
# # # # #             file_context = DATA_PATH.read_text(encoding="utf-8")[:5000]

# # # # #         # 3. Generate Response
# # # # #         combined_context = f"{db_context}\n{file_context}"
# # # # #         formatted_prompt = prompt.format(context=combined_context, input=user_input)
        
# # # # #         # Check topic before final answer
# # # # #         if len(user_input) < 3: return {"answer": "Please ask a valid question about ZT Hosting."}
        
# # # # #         response = llm.invoke(formatted_prompt)
# # # # #         return {"answer": response.content.strip()}
    
# # # # #     except Exception as e:
# # # # #         return {"answer": f"System Error: {str(e)}"}

# # # # # @app.get("/", response_class=HTMLResponse)
# # # # # async def get_home():
# # # # #     if HTML_PATH.exists():
# # # # #         return HTML_PATH.read_text(encoding="utf-8")
# # # # #     return "<h1>Main index.html missing</h1>"



# # # # # Niche diya gaya mukammal code copy karein aur apni api/app.py mein replace kar dein. Ismein maine Login, Admin Panel, Logout, aur Vercel Fixes sab add kar diye hain.



# # # # import os 
# # # # from pathlib import Path
# # # # from fastapi import FastAPI, Request, Form
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from fastapi.responses import HTMLResponse, RedirectResponse
# # # # import requests
# # # # from langchain_groq import ChatGroq
# # # # from langchain_core.prompts import ChatPromptTemplate
# # # # from supabase import create_client, Client 

# # # # app = FastAPI()

# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=["*"],
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )

# # # # # --- Path Configuration ---
# # # # BASE_DIR = Path(__file__).resolve().parent.parent
# # # # DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
# # # # HTML_PATH = BASE_DIR / "templates" / "index.html"
# # # # ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
# # # # LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# # # # # Credentials from Vercel Environment Variables
# # # # ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
# # # # ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
# # # # RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

# # # # # --- Clients Setup ---
# # # # supabase: Client = create_client(os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_KEY", ""))

# # # # def get_llm():
# # # #     return ChatGroq(
# # # #         groq_api_key=os.environ.get("GROQ_API_KEY"), 
# # # #         model_name="llama-3.3-70b-versatile", 
# # # #         temperature=0.1 
# # # #     )

# # # # # --- Helper: Authentication ---
# # # # def check_auth(request: Request):
# # # #     return request.cookies.get("admin_session") == "active"

# # # # # --- Auth Routes ---

# # # # @app.get("/login", response_class=HTMLResponse)
# # # # async def get_login():
# # # #     if LOGIN_HTML_PATH.exists():
# # # #         return LOGIN_HTML_PATH.read_text(encoding="utf-8")
# # # #     return "<h1>Login Page Missing</h1>"

# # # # @app.post("/login")
# # # # async def do_login(username: str = Form(...), password: str = Form(...), g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")):
# # # #     # Verify reCAPTCHA
# # # #     verify_url = "https://www.google.com/recaptcha/api/siteverify"
# # # #     res = requests.post(verify_url, data={"secret": RECAPTCHA_SECRET_KEY, "response": g_recaptcha_response}).json()

# # # #     if not res.get("success"):
# # # #         return HTMLResponse("<h2>Captcha Failed!</h2>", status_code=400)

# # # #     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
# # # #         response = RedirectResponse(url="/admin-zt", status_code=303)
# # # #         response.set_cookie(key="admin_session", value="active", httponly=True, secure=True, samesite="lax")
# # # #         return response
    
# # # #     return HTMLResponse("<h2>Invalid Credentials!</h2>", status_code=401)

# # # # @app.get("/logout")
# # # # async def logout():
# # # #     response = RedirectResponse(url="/login")
# # # #     response.delete_cookie("admin_session")
# # # #     return response

# # # # # --- Protected Admin Routes ---

# # # # @app.get("/admin-zt", response_class=HTMLResponse)
# # # # async def get_admin(request: Request):
# # # #     if not check_auth(request):
# # # #         return RedirectResponse(url="/login", status_code=303)
# # # #     if ADMIN_HTML_PATH.exists():
# # # #         return ADMIN_HTML_PATH.read_text(encoding="utf-8")
# # # #     return "<h1>Admin Page Missing</h1>"

# # # # @app.post("/add-faq")
# # # # async def add_faq(request: Request):
# # # #     if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
# # # #     data = await request.json()
# # # #     supabase.table("manual_faqs").insert({"question": data.get("question").lower(), "answer": data.get("answer")}).execute()
# # # #     return {"status": "success"}

# # # # # --- AI & Main Routes ---

# # # # @app.post("/ask")
# # # # async def ask_bot(request: Request):
# # # #     try:
# # # #         data = await request.json()
# # # #         user_input = data.get("message", "").strip()
# # # #         llm = get_llm()

# # # #         # Database Check
# # # #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# # # #         for row in db_res.data:
# # # #             if row['question'].lower() in user_input.lower():
# # # #                 return {"answer": row['answer']}

# # # #         # AI Fallback
# # # #         prompt = ChatPromptTemplate.from_template("You are ZT Hosting Support. Answer briefly and use **bold** for prices. Context: {context} Question: {input}")
# # # #         context = DATA_PATH.read_text(encoding="utf-8")[:5000] if DATA_PATH.exists() else ""
# # # #         response = llm.invoke(prompt.format(context=context, input=user_input))
# # # #         return {"answer": response.content.strip()}
# # # #     except Exception as e:
# # # #         return {"answer": f"System Error: {str(e)}"}

# # # # @app.get("/", response_class=HTMLResponse)
# # # # async def get_home():
# # # #     if HTML_PATH.exists(): return HTML_PATH.read_text(encoding="utf-8")
# # # #     return "<h1>Chatbot Home</h1>"


# # # Bilkul, main aapko optimized code de raha hoon. Isme maine Path handling ko mazeed mazboot kar diya hai aur ek Debug Route bhi add kiya hai taake aap khud check kar saken ke file load ho rahi hai ya nahi.


# # import os 
# # from pathlib import Path
# # from fastapi import FastAPI, Request, Form
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse, RedirectResponse
# # import requests
# # from langchain_groq import ChatGroq
# # from langchain_core.prompts import ChatPromptTemplate
# # from supabase import create_client, Client 

# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # --- Better Path Configuration ---
# # # Hum 'api/app.py' se start kar rahe hain
# # CURRENT_FILE = Path(__file__).resolve()
# # API_DIR = CURRENT_FILE.parent
# # BASE_DIR = API_DIR.parent  # ZT-HOSTING-CHATBOT-MAIN folder

# # DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
# # HTML_PATH = BASE_DIR / "templates" / "index.html"
# # ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
# # LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# # # Environment Variables
# # ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
# # ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
# # RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

# # # Clients Setup
# # supabase: Client = create_client(os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_KEY", ""))

# # def get_llm():
# #     return ChatGroq(
# #         groq_api_key=os.environ.get("GROQ_API_KEY"), 
# #         model_name="llama-3.3-70b-versatile", 
# #         temperature=0.1 
# #     )

# # # --- Auth Helper ---
# # def check_auth(request: Request):
# #     return request.cookies.get("admin_session") == "active"

# # # --- Debug Route (Bahut Zaroori) ---
# # @app.get("/debug-paths")
# # async def debug_paths():
# #     """Is route ko browser mein open karein (/debug-paths) check karne ke liye"""
# #     return {
# #         "current_file": str(CURRENT_FILE),
# #         "base_dir": str(BASE_DIR),
# #         "data_path_exists": DATA_PATH.exists(),
# #         "data_path_full": str(DATA_PATH),
# #         "templates_exist": {
# #             "index": HTML_PATH.exists(),
# #             "admin": ADMIN_HTML_PATH.exists()
# #         }
# #     }

# # # --- AI & Main Routes ---

# # @app.post("/ask")
# # async def ask_bot(request: Request):
# #     try:
# #         data = await request.json()
# #         user_input = data.get("message", "").strip()
# #         if not user_input:
# #             return {"answer": "Aapka sawal kya hai?"}

# #         llm = get_llm()

# #         # 1. Database Check (Manual FAQs)
# #         db_res = supabase.table("manual_faqs").select("question, answer").execute()
# #         for row in db_res.data:
# #             if row['question'].lower() in user_input.lower() or user_input.lower() in row['question'].lower():
# #                 return {"answer": row['answer']}

# #         # 2. File Context Check
# #         if not DATA_PATH.exists():
# #             return {"answer": "System error: My knowledge base file is missing. Please contact admin."}
        
# #         context_text = DATA_PATH.read_text(encoding="utf-8")

# #         # 3. AI Processing with clear instructions
# #         system_prompt = (
# #             "You are ZT Hosting Support assistant. "
# #             "Use the provided context to answer questions. "
# #             "If the answer is not in context, say 'I am sorry, I don't have this information yet.' "
# #             "Always use **bold** for pricing and keep answers short."
# #         )
        
# #         prompt = ChatPromptTemplate.from_messages([
# #             ("system", system_prompt),
# #             ("user", "Context: {context}\n\nQuestion: {input}")
# #         ])

# #         chain = prompt | llm
# #         response = chain.invoke({"context": context_text[:6000], "input": user_input})
        
# #         return {"answer": response.content.strip()}

# #     except Exception as e:
# #         return {"answer": f"System Error: {str(e)}"}

# # # --- Routes for UI ---

# # @app.get("/", response_class=HTMLResponse)
# # async def get_home():
# #     if HTML_PATH.exists(): return HTML_PATH.read_text(encoding="utf-8")
# #     return "<h1>Chatbot Home (File missing)</h1>"

# # @app.get("/login", response_class=HTMLResponse)
# # async def get_login():
# #     if LOGIN_HTML_PATH.exists(): return LOGIN_HTML_PATH.read_text(encoding="utf-8")
# #     return "<h1>Login Page Missing</h1>"

# # @app.post("/login")
# # async def do_login(username: str = Form(...), password: str = Form(...), g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")):
# #     verify_url = "https://www.google.com/recaptcha/api/siteverify"
# #     res = requests.post(verify_url, data={"secret": RECAPTCHA_SECRET_KEY, "response": g_recaptcha_response}).json()

# #     if not res.get("success"):
# #         return HTMLResponse("<h2>Captcha Failed!</h2>", status_code=400)

# #     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
# #         response = RedirectResponse(url="/admin-zt", status_code=303)
# #         response.set_cookie(key="admin_session", value="active", httponly=True, secure=True, samesite="lax")
# #         return response
    
# #     return HTMLResponse("<h2>Invalid Credentials!</h2>", status_code=401)

# # @app.get("/admin-zt", response_class=HTMLResponse)
# # async def get_admin(request: Request):
# #     if not check_auth(request): return RedirectResponse(url="/login", status_code=303)
# #     if ADMIN_HTML_PATH.exists(): return ADMIN_HTML_PATH.read_text(encoding="utf-8")
# #     return "<h1>Admin Page Missing</h1>"

# # @app.post("/add-faq")
# # async def add_faq(request: Request):
# #     if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
# #     data = await request.json()
# #     supabase.table("manual_faqs").insert({"question": data.get("question").lower(), "answer": data.get("answer")}).execute()
# #     return {"status": "success"}

# # @app.get("/logout")
# # async def logout():
# #     response = RedirectResponse(url="/login")
# #     response.delete_cookie("admin_session")
# #     return response



# # Pura Updated Code (With your original logic)
# # Agar aap chahte hain ke main copy-paste ke liye pura code de doon jisme sirf ye 2 changes hon, toh ye raha:


# import os 
# from pathlib import Path
# from fastapi import FastAPI, Request, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse, RedirectResponse
# import requests
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from supabase import create_client, Client 

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Better Path Configuration ---
# CURRENT_FILE = Path(__file__).resolve()
# API_DIR = CURRENT_FILE.parent
# BASE_DIR = API_DIR.parent 

# DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
# HTML_PATH = BASE_DIR / "templates" / "index.html"
# ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
# LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# # Environment Variables
# ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
# ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
# RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

# # Clients Setup
# supabase: Client = create_client(os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_KEY", ""))

# def get_llm():
#     return ChatGroq(
#         groq_api_key=os.environ.get("GROQ_API_KEY"), 
#         model_name="llama3-8b-8192", # Change 1: Token Saving Model
#         temperature=0.1 
#     )

# # --- Auth Helper ---
# def check_auth(request: Request):
#     return request.cookies.get("admin_session") == "active"

# # --- Debug Route ---
# @app.get("/debug-paths")
# async def debug_paths():
#     return {
#         "current_file": str(CURRENT_FILE),
#         "base_dir": str(BASE_DIR),
#         "data_path_exists": DATA_PATH.exists(),
#         "data_path_full": str(DATA_PATH),
#         "templates_exist": {
#             "index": HTML_PATH.exists(),
#             "admin": ADMIN_HTML_PATH.exists()
#         }
#     }

# # --- AI & Main Routes ---

# @app.post("/ask")
# async def ask_bot(request: Request):
#     try:
#         data = await request.json()
#         user_input = data.get("message", "").strip()
#         if not user_input:
#             return {"answer": "Aapka sawal kya hai?"}

#         llm = get_llm()

#         # 1. Database Check
#         db_res = supabase.table("manual_faqs").select("question, answer").execute()
#         for row in db_res.data:
#             if row['question'].lower() in user_input.lower() or user_input.lower() in row['question'].lower():
#                 return {"answer": row['answer']}

#         # 2. File Context Check
#         if not DATA_PATH.exists():
#             return {"answer": "System error: My knowledge base file is missing."}
        
#         context_text = DATA_PATH.read_text(encoding="utf-8")

#         # 3. AI Processing
#         system_prompt = (
#             "You are ZT Hosting Support assistant. "
#             "Use the provided context to answer questions. "
#             "If the answer is not in context, say 'I am sorry, I don't have this information yet.' "
#             "Always use **bold** for pricing and keep answers short."
#         )
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("user", "Context: {context}\n\nQuestion: {input}")
#         ])

#         chain = prompt | llm
#         # Change 2: Increased Context limit to 10k
#         response = chain.invoke({"context": context_text[:10000], "input": user_input})
        
#         return {"answer": response.content.strip()}

#     except Exception as e:
#         return {"answer": f"System Error: {str(e)}"}

# # --- Routes for UI (Baqi routes same rahenge) ---
# @app.get("/", response_class=HTMLResponse)
# async def get_home():
#     if HTML_PATH.exists(): return HTML_PATH.read_text(encoding="utf-8")
#     return "<h1>Chatbot Home</h1>"

# @app.get("/login", response_class=HTMLResponse)
# async def get_login():
#     if LOGIN_HTML_PATH.exists(): return LOGIN_HTML_PATH.read_text(encoding="utf-8")
#     return "<h1>Login Page Missing</h1>"

# @app.post("/login")
# async def do_login(username: str = Form(...), password: str = Form(...), g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")):
#     verify_url = "https://www.google.com/recaptcha/api/siteverify"
#     res = requests.post(verify_url, data={"secret": RECAPTCHA_SECRET_KEY, "response": g_recaptcha_response}).json()
#     if not res.get("success"): return HTMLResponse("<h2>Captcha Failed!</h2>", status_code=400)
#     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#         response = RedirectResponse(url="/admin-zt", status_code=303)
#         response.set_cookie(key="admin_session", value="active", httponly=True, secure=True, samesite="lax")
#         return response
#     return HTMLResponse("<h2>Invalid Credentials!</h2>", status_code=401)

# @app.get("/admin-zt", response_class=HTMLResponse)
# async def get_admin(request: Request):
#     if not check_auth(request): return RedirectResponse(url="/login", status_code=303)
#     if ADMIN_HTML_PATH.exists(): return ADMIN_HTML_PATH.read_text(encoding="utf-8")
#     return "<h1>Admin Page Missing</h1>"

# @app.post("/add-faq")
# async def add_faq(request: Request):
#     if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
#     data = await request.json()
#     supabase.table("manual_faqs").insert({"question": data.get("question").lower(), "answer": data.get("answer")}).execute()
#     return {"status": "success"}

# @app.get("/logout")
# async def logout():
#     response = RedirectResponse(url="/login")
#     response.delete_cookie("admin_session")
#     return response






# Pura Updated Code (With your original logic)
# Agar aap chahte hain ke main copy-paste ke liye pura code de doon jisme sirf ye 2 changes hon, toh ye raha:



import os 
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from supabase import create_client, Client
from response_formatter import ResponseFormatter
from output_parser import FormattedOutputParser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Better Path Configuration ---
CURRENT_FILE = Path(__file__).resolve()
API_DIR = CURRENT_FILE.parent
BASE_DIR = API_DIR.parent 

DATA_PATH = BASE_DIR / "data" / "zt_data.txt"
HTML_PATH = BASE_DIR / "templates" / "index.html"
ADMIN_HTML_PATH = BASE_DIR / "templates" / "admin.html"
LOGIN_HTML_PATH = BASE_DIR / "templates" / "login.html"

# Environment Variables
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")

# Clients Setup
supabase: Client = create_client(os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_KEY", ""))

def get_llm():
    return ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"), 
        # Updated to a currently supported model
        model_name="llama-3.1-8b-instant", 
        temperature=0.1 
    )

# --- Auth Helper ---
def check_auth(request: Request):
    return request.cookies.get("admin_session") == "active"

# --- Debug Route ---
@app.get("/debug-paths")
async def debug_paths():
    return {
        "current_file": str(CURRENT_FILE),
        "base_dir": str(BASE_DIR),
        "data_path_exists": DATA_PATH.exists(),
        "data_path_full": str(DATA_PATH),
        "templates_exist": {
            "index": HTML_PATH.exists(),
            "admin": ADMIN_HTML_PATH.exists()
        }
    }

# # --- AI & Main Routes ---

# @app.post("/ask")
# async def ask_bot(request: Request):
#     try:
#         data = await request.json()
#         user_input = data.get("message", "").strip()
#         if not user_input:
#             return {"answer": "Aapka sawal kya hai?"}

#         llm = get_llm()

#         # 1. Database Check
#         db_res = supabase.table("manual_faqs").select("question, answer").execute()
#         for row in db_res.data:
#             if row['question'].lower() in user_input.lower() or user_input.lower() in row['question'].lower():
#                 return {"answer": row['answer']}

#         # 2. File Context Check
#         if not DATA_PATH.exists():
#             return {"answer": "System error: My knowledge base file is missing."}
        
#         context_text = DATA_PATH.read_text(encoding="utf-8")

#         # 3. AI Processing
#         system_prompt = (
#             "You are ZT Hosting Support assistant. "
#             "Use the provided context to answer questions. "
#             "If the answer is not in context, say 'I am sorry, I don't have this information yet.' "
#             "Always use **bold** for pricing and keep answers short."
#         )
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("user", "Context: {context}\n\nQuestion: {input}")
#         ])

#         chain = prompt | llm
#         # Change 2: Increased Context limit to 10k
#         response = chain.invoke({"context": context_text[:10000], "input": user_input})
        
#         return {"answer": response.content.strip()}

#     except Exception as e:
#         return {"answer": f"System Error: {str(e)}"}


# update the code to prevent from sorry i dont have this information

# @app.post("/ask")
# async def ask_bot(request: Request):
#     try:
#         data = await request.json()
#         user_input = data.get("message", "").strip()
#         if not user_input:
#             return {"answer": "Aapka sawal kya hai?"}

#         # --- STEP 1: DATABASE CHECK FIRST ---
#         # Hum database se saare FAQs nikal kar check karenge
#         db_res = supabase.table("manual_faqs").select("question, answer").execute()
        
#         for row in db_res.data:
#             # Check agar user ka sawal DB ke kisi sawal se match karta hai
#             if row['question'].lower() in user_input.lower() or user_input.lower() in row['question'].lower():
#                 # Agar DB mein mil jaye toh yahin se jawab de dein (No AI needed)
#                 return {"answer": row['answer']}

#         # --- STEP 2: FILE & AI PROCESSING (Agar DB mein jawab na mile) ---
#         llm = get_llm()

#         if not DATA_PATH.exists():
#             return {"answer": "System error: Knowledge base file is missing."}
        
#         # Optimized context for speed
#         context_text = DATA_PATH.read_text(encoding="utf-8")[:10000]

#         system_prompt = (
#             "You are ZT Hosting Support assistant. "
#             "Priority: Use the tables in the context for pricing. "
#             "Mention both first-month and renewal prices if available. "
#             "If information is not in context, say 'I am sorry, I don't have this information yet.' "
#             "Use **bold** for prices and plan names."
#         )
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("user", "Context: {context}\n\nQuestion: {input}")
#         ])

#         chain = prompt | llm
#         response = chain.invoke({"context": context_text, "input": user_input})
        
#         return {"answer": response.content.strip()}

#     except Exception as e:
#         # Rate limit handling
#         if "429" in str(e):
#             return {"answer": "System is busy. Please try again in 10 minutes."}
#         return {"answer": f"System Error: {str(e)}"}


@app.post("/ask")
async def ask_bot(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "").lower().strip()
        if not user_input:
            return {"answer": "Aapka sawal kya hai?"}

        # --- LOAD BOT SETTINGS ---
        try:
            settings_res = supabase.table("bot_settings").select("*").limit(1).execute()
            if settings_res.data and len(settings_res.data) > 0:
                settings = settings_res.data[0]
                response_style = settings.get("response_style", "short")
                priority = settings.get("priority", "database_first")
                context_size = settings.get("context_size", 4000)
            else:
                # Defaults
                response_style = "short"
                priority = "database_first"
                context_size = 4000
        except:
            # Defaults if table doesn't exist yet
            response_style = "short"
            priority = "database_first"
            context_size = 4000

        # --- STEP 1: DATABASE CHECK ---
        db_res = supabase.table("manual_faqs").select("question, answer").execute()
        db_context = ""  # Initialize db_context
        
        if priority == "database_first":
            # Strict database priority - return immediately on match
            for row in db_res.data:
                if row['question'].lower() in user_input:
                    # Apply OutputParser to database answers too
                    output_parser = FormattedOutputParser(style=response_style, user_input=user_input)
                    result = output_parser.parse(row['answer'])
                    return {
                        "answer": result["final_text"],
                        "metadata": {
                            "tokens_used": result["tokens_used"],
                            "truncated": result["truncated"],
                            "source": "database"
                        }
                    }
        else:
            # AI supplement mode - collect DB context but don't return yet
            for row in db_res.data:
                if row['question'].lower() in user_input:
                    db_context = f"Database Info: {row['answer']}\n\n"
                    break

        # --- STEP 2: SMART FILE ROUTING ---
        # Default file: Agar koi specific keyword na mile toh home page ya general info use karein
        file_name = "zt_home_page.txt" 
        
        if "reseller" in user_input:
            file_name = "reseller_hosting.txt"
        elif any(x in user_input for x in ["domain", ".pk", ".com", "register"]):
            file_name = "domain_registration.txt"
        elif "vps" in user_input:
            file_name = "pro_vps_hosting.txt"
        elif "business" in user_input:
            file_name = "pro_hosting_business_web.txt"
        elif "wordpress" in user_input:
            file_name = "pro_wordpress_hosting.txt"
        elif "email" in user_input:
            file_name = "pro_email_hosting.txt"
        elif "dedicated" in user_input:
            file_name = "pro_dedicated_servers.txt"
        elif "promo" in user_input or "offer" in user_input:
            file_name = "promo_packages.txt"
        elif "shared" in user_input or "web hosting" in user_input:
            file_name = "shared_webhosting.txt"

        target_path = BASE_DIR / "data" / file_name
        
        # Sirf tabhi parhein agar file exist karti ho
        if target_path.exists():
            # Use dynamic context size from settings
            file_context = target_path.read_text(encoding="utf-8")[:context_size]
        else:
            return {"answer": "I am sorry, I don't have specific details about this service yet."}

        # --- STEP 3: AI PROCESSING ---
        llm = get_llm()
        
        # Build system prompt based on response style
        if response_style == "conversational":
            system_prompt = (
                "You are a friendly and helpful ZT Hosting Support assistant. "
                "Answer in a conversational, human-like tone with warmth and empathy. "
                "Feel free to use greetings and be detailed in your explanations. "
                "### CRITICAL INSTRUCTION for Pricing: ### "
                "1. For any plan price, FIRST look at the Markdown Tables. "
                "2. If a table shows a '$1/1st month' offer, you MUST mention it with enthusiasm. "
                "3. Format pricing clearly: 'Great news! You can start with just **$1 for the 1st month**, "
                "and then it renews at **PKR [Price]**'. "
                "4. If info like 'cPanel accounts' or 'SSD Storage' is in a table, extract it accurately. "
                "5. If you cannot find the answer, politely say 'I apologize, but I don't have that specific "
                "information at the moment. Let me connect you with our support team who can help you better.'"
            )
        else:
            # Short and professional
            system_prompt = (
                "You are ZT Hosting Support assistant. Answer ONLY based on the provided context. "
                "Keep responses concise and to-the-point. "
                "### CRITICAL INSTRUCTION for Pricing: ### "
                "1. For any plan price, FIRST look at the Markdown Tables. "
                "2. If a table shows a '$1/1st month' offer, you MUST mention it. Do not just say the PKR price. "
                "3. Format pricing clearly: 'Promo: **$1 for the 1st month**, Renewing at: **PKR [Price]**'. "
                "4. If info like 'cPanel accounts' or 'SSD Storage' is in a table, extract it accurately from the correct column. "
                "5. If you cannot find the answer in the provided text, say 'I am sorry, I don't have this information yet.'"
            )
        
        # Combine contexts if in AI supplement mode and db_context exists
        if priority == "ai_supplement" and db_context:
            context_text = db_context + file_context
        else:
            context_text = file_context
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", f"Context: {context_text}\n\nQuestion: {user_input}")
        ])

        # Create OutputParser with current settings
        output_parser = FormattedOutputParser(style=response_style, user_input=user_input)
        
        # Wire OutputParser into chain via RunnableSequence
        chain = prompt | llm | output_parser
        
        # Invoke the chain - parser returns structured output
        result = chain.invoke({"input": user_input})
        
        # Return the formatted text with metadata
        return {
            "answer": result["final_text"],
            "metadata": {
                "tokens_used": result["tokens_used"],
                "truncated": result["truncated"]
            }
        }

    except Exception as e:
        # Code 413 or 429 management
        if "413" in str(e) or "limit" in str(e).lower():
            return {"answer": "The request is too large or system is busy. Please try asking a shorter question."}
        return {"answer": f"System Error: {str(e)}"}


# --- Routes for UI (Baqi routes same rahenge) ---
@app.get("/", response_class=HTMLResponse)
async def get_home():
    if HTML_PATH.exists(): return HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Chatbot Home</h1>"

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    if LOGIN_HTML_PATH.exists(): return LOGIN_HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Login Page Missing</h1>"

@app.post("/login")
async def do_login(username: str = Form(...), password: str = Form(...), g_recaptcha_response: str = Form(None, alias="g-recaptcha-response")):
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    res = requests.post(verify_url, data={"secret": RECAPTCHA_SECRET_KEY, "response": g_recaptcha_response}).json()
    if not res.get("success"): return HTMLResponse("<h2>Captcha Failed!</h2>", status_code=400)
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin-zt", status_code=303)
        response.set_cookie(key="admin_session", value="active", httponly=True, secure=True, samesite="lax")
        return response
    return HTMLResponse("<h2>Invalid Credentials!</h2>", status_code=401)

@app.get("/admin-zt", response_class=HTMLResponse)
async def get_admin(request: Request):
    if not check_auth(request): return RedirectResponse(url="/login", status_code=303)
    if ADMIN_HTML_PATH.exists(): return ADMIN_HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Admin Page Missing</h1>"

@app.post("/add-faq")
async def add_faq(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    
    if not question or not answer:
        return {"status": "error", "message": "Question and answer are required"}
    
    if len(question) > 500:
        return {"status": "error", "message": "Question too long (max 500 characters)"}
    
    if len(answer) > 5000:
        return {"status": "error", "message": "Answer too long (max 5000 characters)"}
    
    try:
        supabase.table("manual_faqs").insert({"question": question.lower(), "answer": answer}).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.get("/get-faqs")
async def get_faqs(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    try:
        response = supabase.table("manual_faqs").select("*").order("id", desc=True).execute()
        return {"status": "success", "faqs": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.put("/update-faq")
async def update_faq(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    faq_id = data.get("id")
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    
    if not isinstance(faq_id, int) or faq_id <= 0:
        return {"status": "error", "message": "Invalid FAQ ID"}
    
    if not question or not answer:
        return {"status": "error", "message": "Question and answer are required"}
    
    if len(question) > 500:
        return {"status": "error", "message": "Question too long (max 500 characters)"}
    
    if len(answer) > 5000:
        return {"status": "error", "message": "Answer too long (max 5000 characters)"}
    
    try:
        supabase.table("manual_faqs").update({
            "question": question.lower(),
            "answer": answer
        }).eq("id", faq_id).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.delete("/delete-faq")
async def delete_faq(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    faq_id = data.get("id")
    
    if not isinstance(faq_id, int) or faq_id <= 0:
        return {"status": "error", "message": "Invalid FAQ ID"}
    
    try:
        supabase.table("manual_faqs").delete().eq("id", faq_id).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.get("/get-settings")
async def get_settings(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    try:
        response = supabase.table("bot_settings").select("*").limit(1).execute()
        if response.data and len(response.data) > 0:
            return {"status": "success", "settings": response.data[0]}
        else:
            # Return defaults
            return {
                "status": "success",
                "settings": {
                    "response_style": "short",
                    "priority": "database_first",
                    "context_size": 4000
                }
            }
    except Exception as e:
        # Return defaults on error
        return {
            "status": "success",
            "settings": {
                "response_style": "short",
                "priority": "database_first",
                "context_size": 4000
            }
        }

@app.post("/save-settings")
async def save_settings(request: Request):
    if not check_auth(request): return {"status": "error", "message": "Unauthorized"}
    data = await request.json()
    
    # Input validation
    response_style = data.get("response_style")
    priority = data.get("priority")
    context_size = data.get("context_size")
    
    # Validate response_style
    if response_style not in ["short", "conversational"]:
        return {"status": "error", "message": "Invalid response_style"}
    
    # Validate priority
    if priority not in ["database_first", "ai_supplement"]:
        return {"status": "error", "message": "Invalid priority"}
    
    # Validate context_size
    if not isinstance(context_size, int) or context_size not in [2000, 4000, 6000]:
        return {"status": "error", "message": "Invalid context_size"}
    
    try:
        # Check if settings exist
        existing = supabase.table("bot_settings").select("*").limit(1).execute()
        
        settings_data = {
            "response_style": response_style,
            "priority": priority,
            "context_size": context_size
        }
        
        if existing.data and len(existing.data) > 0:
            # Update existing
            supabase.table("bot_settings").update(settings_data).eq("id", existing.data[0]["id"]).execute()
        else:
            # Insert new
            supabase.table("bot_settings").insert(settings_data).execute()
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": "Database error"}

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("admin_session")
    return response