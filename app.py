from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
import tempfile
from Embedding_fuctions.embeddings import Model,get_full_text,split_text,combine_pdfs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import shutil
import os
import json
from database.mongodb import insert_or_update_study,get_all_studies,get_collections_by_study
from chat_functions.chats import get_collection ,query_collection,rag,delete_collection,get_collection_names
from Excel_chat_bot.excel_fun import*
import tempfile
import uuid
from config import settings

app = FastAPI(title=settings.APP_NAME)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

model = Model()
# Connect to ChromaDB using config settings
chroma_client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
@app.post("/upload_pdf/")
async def combine_pdfs_endpoint(files: list[UploadFile], collection_name: str):
    # Create a directory to save uploaded files
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, mode=0o777, exist_ok=True)
    
    pdf_paths = []
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        # Write file with proper handling
        try:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            # Ensure file has read/write permissions
            os.chmod(file_path, 0o666)
        except PermissionError as e:
            raise HTTPException(status_code=500, detail=f"Permission denied: Unable to write to {file_path}. Please check directory permissions.")
        pdf_paths.append(file_path)
    output_filename = settings.COMBINED_PDF
    combine_pdfs(pdf_paths, output_filename)
    full_text = get_full_text(output_filename)   
    split_text_d=split_text(full_text)
    print(type(split_text_d))
    try:
        try:
            collection=chroma_client.get_collection(name=collection_name, embedding_function=model)
        except:
            collection=chroma_client.create_collection(name=collection_name, embedding_function=model)
    except Exception as e:
        # Better error message parsing
        error_msg = str(e)
        if "'" in error_msg:
            try:
                error_msg = error_msg.split("'")[1]
            except IndexError:
                pass  # Keep the full error message
        return JSONResponse(content={"Error": error_msg}, status_code=409)
    ids = [str(uuid.uuid4()) for _ in range(len(split_text_d))]
    collection.add(ids=ids, documents=split_text_d)
    Data_in_collecction=collection.count()
    #insert_or_update_study(study,collection_name)
    return JSONResponse(content={"message": "PDF uploaded and processed successfully.", "total_chunks": len(split_text_d),"Data_in_collecction":Data_in_collecction})
@app.post("/upload_excel")
async def upload_excel_endpoint(files:list[UploadFile], collection_name: str):
    text_data_list = []

    # Process each file
    for file in files:
        if file.filename.endswith('.xlsx'):
            # Save the file temporarily
            temp_file_path = get_temp_file_path(file.filename)
            with open(temp_file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Convert the Excel file to text
            text_data = excel_to_text(temp_file_path)
            text_data_list.append(text_data)
        else:
            raise HTTPException(status_code=400, detail=f'File {file.filename} is not an Excel file')

    # Prepare data for ChromaDB
    split_text_d = text_data_list
    #ids = [str(i) for i in range(len(split_text_d))]
    ids = [str(uuid.uuid4()) for _ in range(len(split_text_d))]
    try:
        try:
            collection=chroma_client.get_collection(name=collection_name, embedding_function=model)
        except:
            collection=chroma_client.create_collection(name=collection_name, embedding_function=model)
        collection.add(ids=ids, documents=split_text_d)
        data_in_collection = collection.count()
    except Exception as e:
        # Better error message parsing
        error_msg = str(e)
        if "'" in error_msg:
            try:
                error_msg = error_msg.split("'")[1]
            except IndexError:
                pass  # Keep the full error message
        return JSONResponse(content={"Error": error_msg}, status_code=409)

    return JSONResponse(
        content={
            "message": "Excel files uploaded and processed successfully.",
            "total_chunks": len(split_text_d),
            "data_in_collection": data_in_collection
        }
    )
class QueryRequest(BaseModel):
    question: str
    collection_name: str


@app.post('/ask')
async def ask(query_request: QueryRequest):
    query = query_request.question
    collection_name = query_request.collection_name
    print(collection_name)

    if not query or not collection_name:
        raise HTTPException(status_code=400, detail="Missing 'question' or 'collection_name'")

    model = Model()
    try:
        collection_G=get_collection(collection_name,model)
    except Exception as e:
        return {"Error":"collection_name not found"}    
    
    retrieved_documents = query_collection(collection_G, query)
    
    if not retrieved_documents:
        raise HTTPException(status_code=404, detail="No documents retrieved")

    # Call RAG with error handling for Ollama connection
    try:
        answer = rag(query, retrieved_documents)
        return {"answer": answer}
    except Exception as e:
        error_message = str(e)
        if "Connection error" in error_message or "ConnectError" in error_message:
            raise HTTPException(
                status_code=503, 
                detail="Cannot connect to Ollama LLM service. Please ensure Ollama is running on the server (port 11434) and the llama3.2:3b model is installed."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Error generating answer: {error_message}")

@app.delete('/delete-collection/{name}')
async def delete_collection_endpoint(name: str):
    response = delete_collection(name)
    if "Failed" in response["message"]:
        raise HTTPException(status_code=400, detail=response["message"])
    return response
# @app.get('/study')
# async def get_studies_with_collections():
#     studies = get_all_studies()
#     # Assuming each study document has a 'study' field with the name of the study
#     # and a 'collection_names' field with a list of associated collection names
#     studies_with_collections = [
#         {
#             "study": study['study'],
#             "collections": study.get('collection_names', [])
#         }
#         for study in studies
#     ]
#     return studies_with_collections
# class CollectionRequest(BaseModel):
#     study: str

# @app.post('/get_collections')
# async def get_collections_with_study(request_body: CollectionRequest):
#     collections = get_collections_by_study(request_body.study)
#     if collections is not None:
#         return {"collections": collections}
#     else:
#         raise HTTPException(status_code=404, detail="Study not found")

# Make sure to include all necessary imports and function definition
@app.get('/get-collection')
async def get_collection_endpoint():
    try:
        response = get_collection_names()
        return JSONResponse(content=response)
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    
