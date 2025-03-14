from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import textwrap
import subprocess

comment1 = "Thats a great Repository. I want to suggest that you should implement search functionality in the users section."
comment2 = 'Thank you'
comment3 = 'Free Money. register now!!!'
