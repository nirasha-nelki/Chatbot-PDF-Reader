# Chatbot PDF Reader

This application is a conversational AI assistant that can answer questions based on the contents of PDF documents. It utilizes LangChain, FAISS, Pinecone, and Streamlit to build a chat interface that interacts with users in real time.

## Features

- **Conversational AI**: Ask questions related to the content of the uploaded PDF documents.
- **Document Retrieval**: Retrieve relevant information from large documents.
- **Supports Pinecone and FAISS**: Optionally use Pinecone for vector storage or FAISS for local vector storage.
- **Streamlit UI**: User-friendly interface to interact with the AI assistant.

## Prerequisites

- Python 3.8 or later
- Virtual environment (optional but recommended)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/nirasha-nelki/Chatbot-PDF-Reader.git
    cd chatbot-pdf-reader
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables by creating a `.env` file in the root directory with the following content:
    ```env
    PINECONE_API_KEY=your_pinecone_api_key
    INDEX=your_pinecone_index_name
    GROQ_API_KEY=your_groq_api_key
    ```

5. If you plan to use Pinecone, ensure that the `pincecone_flag` is set to `True` in `backend.py`. Otherwise, leave it as `False` to use FAISS.

## Usage

1. **Ingest Documents**: Run the following command to ingest documents into Pinecone (if using Pinecone):
    ```bash
    python uploaddocs.py
    ```

2. **Run the Streamlit App**: Start the application by running:
    ```bash
    streamlit run chatui.py
    ```

3. **Interact with the Chatbot**: Open the provided URL in your web browser, and start asking questions based on the uploaded documents.

## Application Structure

- **chatui.py**: The main Streamlit app file that sets up the chat UI and handles user interactions.
- **backend.py**: Contains the logic for interacting with the language model, managing chat history, and retrieving relevant document sections.
- **uploaddocs.py**: Handles document ingestion into Pinecone, splitting the document into manageable chunks, and storing them in the vector store.
- **requirements.txt**: List of Python packages required to run the application.
- **doc/**: A folder to store the documents (PDF files) that will be used by the chatbot.


## Acknowledgements

This project uses [LangChain](https://github.com/hwchase17/langchain), [Streamlit](https://streamlit.io/), [Pinecone](https://www.pinecone.io/), and [FAISS](https://github.com/facebookresearch/faiss).
