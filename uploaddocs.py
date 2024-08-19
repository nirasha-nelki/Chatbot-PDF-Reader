import os
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings()

api_key_pinecone = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key_pinecone)

index=os.getenv("INDEX")

vectorstore = PineconeVectorStore(index_name=index, embedding=embeddings)

def ingest_to_pinecone():
    pdf_folder_path = "doc/"
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith(".pdf"):  # Check if the file is a PDF
            pdf_path = os.path.join(pdf_folder_path, filename)
            print(pdf_path)
            # Load and process the file
            loader = PyPDFLoader(file_path=pdf_path)
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=100, chunk_overlap=20
            )
            chunks = text_splitter.split_documents(data)

            vectorstore.add_documents(chunks)

    return True

# ingest_to_pinecone()