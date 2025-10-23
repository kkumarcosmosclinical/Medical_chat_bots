from chromadb import Documents, EmbeddingFunction, Embeddings
import chromadb.utils.embedding_functions as embedding_functions
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Example OpenAI Embedding Function (commented out)
# class MyEmbeddingFunction(EmbeddingFunction):
#     def __init__(self):
#         import os
#         self.ef = embedding_functions.OpenAIEmbeddingFunction(
#             api_key=os.getenv('OPENAI_API_KEY'),  # Use environment variable
#             model_name="text-embedding-ada-002"
#         )
#     def __call__(self, input: Documents) -> Embeddings:
#         embeddings = self.ef(input)
#         return embeddings
    
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from typing import List, Union

# Define type aliases for clarity
Documents = Union[List[str], str]
Embeddings = List[List[float]]

class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.ef = OllamaEmbeddingFunction(
            url="http://localhost:11434",
            model_name="llama3.2:3b"
        )
    
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self.ef(input)
        return embeddings
def Model():
    model = MyEmbeddingFunction()
    return model


def get_full_text(pdf_path):
    """Return the full text of the PDF."""
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text = page.get_text()
        full_text += text
    return full_text



def split_text(full_text, chunk_size=512, chunk_overlap=20):
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return character_splitter.split_text(full_text)



def combine_pdfs(pdf_files, output_filename):
    combined_pdf = fitz.open()

    for pdf_file in pdf_files:
        pdf_document = fitz.open(pdf_file)
        
        for page_num in range(pdf_document.page_count):
            combined_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        
        pdf_document.close()
    
    combined_pdf.save(output_filename)
    combined_pdf.close()