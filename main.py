# import os
# from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA

# # .env file se API keys load karna
# load_dotenv()

# def start_chat():
#     # 1. Embeddings load karein (Same model jo ingest.py mein tha)
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     # 2. Vector Database se connect karein
#     vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)

#     # 3. Groq LLM Setup
#     llm = ChatGroq(
#         groq_api_key=os.getenv("GROQ_API_KEY"),
#         model_name="llama-3.3-70b-versatile",
#         temperature=0.2
#     )

#     # 4. Retrieval Chain (Database + AI)
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vector_db.as_retriever(search_kwargs={"k": 5}) # Top 5 relevant chunks uthayega
#     )

#     print("\n" + "="*50)
#     print("   ZT HOSTING CHATBOT ACTIVE! (Type 'exit' to quit)")
#     print("="*50)
    
#     while True:
#         user_input = input("\nAapka Sawal: ")
        
#         if user_input.lower() == 'exit':
#             print("Chatbot band ho raha hai. Allah Hafiz!")
#             break
        
#         if not user_input.strip():
#             continue

#         print("Bot soch raha hai...")
        
#         try:
#             # AI se jawab mangein
#             response = qa_chain.invoke(user_input)
#             print(f"\nJawab: {response['result']}")
#         except Exception as e:
#             print(f"Error: {e}")

# if __name__ == "__main__":
#     start_chat()



import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

# 1. Environment variables load karein (.env file se)
load_dotenv()

def start_chat():
    print("Chatbot initialize ho raha hai...")

    # 2. Embeddings load karein (Ye wahi model hai jo ingest.py mein use hua)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Vector Database (db folder) se connect karein
    if not os.path.exists("./db"):
        print("Error: 'db' folder nahi mila. Pehle 'python ingest.py' chalayein.")
        return
        
    vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)

    # 4. Groq LLM Setup
    # Ensure karein ke aapne .env mein GROQ_API_KEY dali hui hai
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    # 5. Prompt Template: Bot ko batana ke wo kaun hai
    prompt = ChatPromptTemplate.from_template("""
    You are a professional and helpful customer support assistant for ZT Hosting. 
    Your goal is to answer questions based strictly on the provided context.
    If the answer is not in the context, politely say that you don't have that information 
    and suggest they contact ZT Hosting support.
    
    Context: {context}
    
    Question: {input}
    
    Answer:""")

    # 6. Chain Setup (Retriever + LLM)
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(vector_db.as_retriever(), document_chain)

    print("\n" + "="*50)
    print("   ZT HOSTING CHATBOT ACTIVE! (Type 'exit' to quit)")
    print("="*50)
    
    while True:
        user_input = input("\nAapka Sawal: ")
        
        if user_input.lower() == 'exit':
            print("Allah Hafiz! Phir milenge.")
            break
        
        if not user_input.strip():
            continue

        print("Bot soch raha hai...")
        
        try:
            # Bot se jawab mangein
            response = retrieval_chain.invoke({"input": user_input})
            print(f"\nJawab: {response['answer']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_chat()