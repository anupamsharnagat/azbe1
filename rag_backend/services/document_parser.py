from langchain_community.document_loaders import PyMuPDFLoader
import os

def extract_text_and_tables_from_pdf(pdf_path: str):
    
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    return documents
