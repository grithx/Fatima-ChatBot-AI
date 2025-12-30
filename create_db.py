import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma

# 1. Apna data load karein
# Ensure karein ke 'data.txt' mein aapka ZT Hosting ka saara data mojud hai
# loader = TextLoader("data.txt", encoding="utf-8")


# loader = TextLoader("zt_data.txt", encoding="utf-8")


loader = TextLoader("data/zt_data.txt", encoding="utf-8")
documents = loader.load()


# 2. Text ko chunks mein divide karein
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 3. FastEmbed Model select karein (Small and Fast)
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# 4. Database banayein aur save karein
print("Database ban raha hai, thora intezar karein...")

db_path = "./db"
vector_db = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings, 
    persist_directory=db_path
)

print(f"Mubarak ho! Naya database '{db_path}' folder mein save ho gaya hai.")