from fastapi import FastAPI
import chromadb
from models import *

def get_chroma_client(persistent: bool = False):
    if persistent :
        # Get a chromadb persistent (data remains after the end of the execution) client
        client = chromadb.PersistentClient(path="./db")
    else:
        # Get the non-persistent chroma client
        client = chromadb.Client()
    
    return client

testPersistent = True

if not testPersistent :
    # Get the chroma client and set it to use duckdb+parquet (a normal db like sqlite3 and the parquet file format [which is column oriented])
    client = chromadb.Client()
else:
    # Get a chromadb persistent (data remains after the end of the execution) client
    client = chromadb.PersistentClient(path="./db")

# Create a collection (think of it like it's an sql table)
collection = client.get_or_create_collection(name="Students")

print(client.list_collections())

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

@app.post("/chroma/collections/")
async def create_collection(chromaCollection: ChromaCollection):

    try:
        client = get_chroma_client(chromaCollection.isPersistent)
        client.get_or_create_collection(name = chromaCollection.name)
        return {'message:' : f'Successfully created new chroma collection "{chromaCollection.name}"'}
    except:
        return {'message:' : 'An error ocurred when creating the new chroma collection'}
    
@app.get("/chroma/collections/")
async def get_collections(isPersistent : bool = False):

    client = get_chroma_client(isPersistent)
    chromaCollections = [collection.name for collection in client.list_collections()]

    return {'Persistent Collections' : isPersistent, 'collections': chromaCollections}