from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from typing import List

testPersistent = True

if not testPersistent :
    # Get the chroma client and set it to use duckdb+parquet (a normal db like sqlite3 and the parquet file format [which is column oriented])
    client = chromadb.Client()
else:
    # Get a chromadb persistent (data remains after the end of the execution) client
    client = chromadb.PersistentClient(path="./db")

# Create a collection (think of it like it's an sql table)
collection = client.get_or_create_collection(name="Students")

class ChromaPrompt(BaseModel):
    userPrompt: str
    collection: str | None = None
    n_results: int | None = 1

class ChromaResult(BaseModel):
    id: str
    source: str
    info: str
    
class Embedding(BaseModel):
    userPrompt: str
    resources: List

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

def append_result(chromaResults: chromadb.QueryResult):
    results = []
    for i in range(0, len(chromaResults['ids'][0])):
        result = ChromaResult(id = chromaResults['ids'][0][i], source = chromaResults['metadatas'][0][i]['source'], info = chromaResults['documents'][0][i])
        results.append(result)
    
    return results

@app.post("/chroma/")
async def get_chroma_embeddings(chromaQuery: ChromaPrompt):

    results = collection.query(
        query_texts = [chromaQuery.userPrompt],
        n_results = chromaQuery.n_results
    )

    response = Embedding(userPrompt=chromaQuery.userPrompt, resources=append_result(results) )
    return response
