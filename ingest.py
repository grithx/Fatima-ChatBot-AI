# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma

# # 1. Load Environment Variables
# load_dotenv()

# def create_vector_db():
#     # 2. Data Load karein
#     print("Loading data...")
#     loader = DirectoryLoader('data/', glob="./*.txt", loader_cls=TextLoader)
#     documents = loader.load()

#     # 3. Text ko chote tukron (Chunks) mein torein
#     # Is se bot ko sahi jawab dhoondne mein asani hoti hai
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = text_splitter.split_documents(documents)

#     # 4. Open Source Embedding Model use karein (English ke liye best hai)
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     # 5. ChromaDB mein save karein
#     print("Creating Vector Database...")
#     vector_db = Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory="./db"
#     )
#     print("Done! Your 'db' folder is ready.")

# if __name__ == "__main__":
#     create_vector_db()


import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def create_vector_db():
    print("Loading data...")
    if not os.path.exists('data'):
        print("Error: 'data' folder nahi mila!")
        return

    # Encoding ko utf-8 set karna zaroori hai
    try:
        loader = DirectoryLoader(
            'data/', 
            glob="*.txt", 
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'} # <--- Ye line error theek karegi
        )
        documents = loader.load()
        print(f"Documents loaded: {len(documents)}")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    if len(documents) == 0:
        print("Error: Koi data nahi mila!")
        return

    # Text Split karein
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # ChromaDB
    print("Creating Vector Database...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./db"
    )
    print("Done! Your 'db' folder is ready.")

if __name__ == "__main__":
    create_vector_db()