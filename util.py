from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import textwrap
import subprocess


def load_pdf_data(file_path):
    loader = PyMuPDFLoader(file_path=file_path)
    return loader.load()

def load_text_data(file_path):
    loader = TextLoader(file_path)
    return loader.load()

def load_doc_data(file_path):
    loader = Docx2txtLoader(file_path)
    return loader.load()

def load_data(file_path):
    if file_path.endswith(".pdf"):
        return load_pdf_data(file_path)
    elif file_path.endswith(".txt"):
        return load_text_data(file_path)
    elif file_path.endswith(".docx"):
        return load_doc_data(file_path)
    else:
        raise ValueError("Unsupported file format")

def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents=documents)



def load_embedding_model(model_path, normalize_embedding=True):
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device':'cpu'},
        encode_kwargs = {
            'normalize_embeddings': normalize_embedding
        }
    )


def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(storing_path)
    return vectorstore

template = """
### System:
You are an respectful and honest assistant. You have to answer the user's \
questions using only the context provided to you. If you don't know the answer, \
just say you don't know. Don't try to make up an answer.

### Context:
{context}

### User:
{question}

### Response:
"""

def load_qa_chain(retriever, llm, prompt):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )


def get_response(query, chain):
    response = chain({'query': query})
    wrapped_text = textwrap.fill(response['result'], width=100)
    return wrapped_text


def list_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        firsts = [line.split()[0] for line in lines]
        return firsts[firsts.index("NAME")+1:]
    except subprocess.CalledProcessError as e:
        print("Error: " + e.stderr)
        return []