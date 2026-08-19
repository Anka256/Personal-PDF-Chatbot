import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma

load_dotenv()

def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return docs

def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunked_docs = text_splitter.split_documents(docs)
    return chunked_docs

def create_vector_store(chunks):
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        dimensions=1024
    )
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
    )

    return vector_store
