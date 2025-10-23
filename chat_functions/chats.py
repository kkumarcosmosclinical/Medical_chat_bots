from Embedding_fuctions.embeddings import Model
import chromadb
from dotenv import load_dotenv
import os
import sys
import openai
from openai import OpenAI

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

load_dotenv()  # Load environment variables from .env file

embedding_function = Model()

# OpenAI client configuration (using local Ollama)
openai_client = OpenAI(
    base_url=f'http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)

# ChromaDB client using config settings
chroma_client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
# openai.api_key = api_key
from fastapi import FastAPI, HTTPException

def get_collection(name, embedding_function):
    try:
        collection = chroma_client.get_collection(name=name, embedding_function=embedding_function)
        print("Pass")
        return collection
    except Exception as e:
        raise HTTPException(status_code=404, detail="Collection not found")


def delete_collection(name):
    try:
        chroma_client.delete_collection(name=name)
        return {"message": "Collection deleted"}
    except Exception as e:
        return {"message": f"Failed to delete collection: {e}"}



def query_collection(collection, query, n_results=10):
    results = collection.query(query_texts=[query], n_results=n_results)
    retrieved_documents = results['documents'][0]
    return retrieved_documents



def rag(query, retrieved_documents, model="llama3.2:3b"):
    information = "\n\n".join(retrieved_documents)

    messages = [
        {
            "role": "system",
            
            "content": """You are a helpful expert medical research assistant. Your users are asking questions about information contained in a medical data PDF report. Please ensure the answers are provided in a point-by-point format for clarity. Additionally, format the answers to be properly readable.

You will be shown the user's question and the relevant information from the annual report. Answer the user's question using only this information."""
           
        },
        {"role": "user", "content": f"Question: {query}. \n Information: {information}"}
    ]
    
    response = openai_client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
    
    content = response.choices[0].message.content
    return content
import requests

def get_collection_names():
    #url = f'http://{settings.CHROMA_HOST}:{settings.CHROMA_PORT}/api/v1/collections'
    url=f'http://{settings.CHROMA_HOST}:{settings.CHROMA_PORT}/api/v2/tenants/default_tenant/databases/default_database/collections'
    tenant = 'default_tenant'
    database = 'default_database'
    # Make the GET request to the specified URL with query parameters
    response = requests.get(
        url,
        params={'tenant': tenant, 'database': database},
        headers={'accept': 'application/json'}
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        collections = response.json()
        
        # Extract names from the collections
        names = [collection['name'] for collection in collections]
        
        return names
    else:
        # Handle errors or unsuccessful requests
        response.raise_for_status()