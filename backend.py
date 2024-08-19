import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage

from uploaddocs import vectorstore

load_dotenv()

pincecone_flag = False ## change this to True if you are using pinecone
embeddings = HuggingFaceEmbeddings()


## import GROQ
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groq_api_key)

if not pincecone_flag:
    loader = PyPDFLoader("doc/sample.txt") ## change the path to the pdf file
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(pages)
    vectorstore = FAISS.from_documents(documents, embeddings)

# Initialize the retriever
if pincecone_flag:
    retriever = vectorstore.as_retriever(search_type="mmr")
else:
    retriever = vectorstore.as_retriever()

# Create a retrieval chain with a history-aware retriever
prompt_with_history = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt_with_history)

# Set up the document chain
prompt_with_context = ChatPromptTemplate.from_messages([
    ("system", """
     
    You are a helpful AI assistant who answers the questions ask from the given PDF document.
    Answer the following question based only on the provided context below. 
    If you can't answer the question, reply "I don't know".
    If the question asked in singlish replay in Sinhala

    Context: {context}
     
     """
     
     ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, prompt_with_context)

# Create the retrieval chain
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

# Define and update chat history with previously asked questions
chat_history = []

# Function to interactively ask questions and get responses
def ask_question(question):
    chat_history.append(HumanMessage(content=question))
    response = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": question
    })
    chat_history.append(AIMessage(content=response["answer"]))
    return response["answer"]
