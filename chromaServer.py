from fastapi import FastAPI
import chromadb
from models import *

def get_chroma_client(persistent: bool = False) -> chromadb.ClientAPI:
    if persistent :
        # Get a chromadb persistent (data remains after the end of the execution) client
        client = chromadb.PersistentClient(path="./db")
    else:
        # Get the non-persistent chroma client
        client = chromadb.Client()
    
    return client

def format_chroma_resutls(chromaResults: chromadb.QueryResult) -> List[ChromaResult]:
    formatted_results = []
    for i in range(0, len(chromaResults['ids'][0])):
        result = ChromaResult(id = chromaResults['ids'][0][i], source = chromaResults['metadatas'][0][i]['source'], info = chromaResults['documents'][0][i])
        formatted_results.append(result)
    
    return formatted_results

app = FastAPI()

@app.post("/chroma/")
async def get_chroma_embeddings(chromaQuery: ChromaPrompt):

    client = get_chroma_client(chromaQuery.isPersistent)
    collection = client.get_collection(chromaQuery.collectionName)

    results = collection.query(
        query_texts = [chromaQuery.userPrompt],
        n_results = chromaQuery.n_results
    )
    response = InContextResponse(userPrompt=chromaQuery.userPrompt, resources=format_chroma_resutls(results) )
    
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