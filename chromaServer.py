from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
from typing import List


student_info = """
Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
in her free time in hopes of working at a tech company after graduating from the University of Washington.
"""

club_info = """
The university chess club provides an outlet for students to come together and enjoy playing
the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
participate in tournaments, analyze famous chess matches, and improve members' skills.
"""

university_info = """
The University of Washington, founded in 1861 in Seattle, is a public research university
with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
As the flagship institution of the six public universities in Washington state,
UW encompasses over 500 buildings and 20 million square feet of space,
including one of the largest library systems in the world.
"""

testPersistent = True

if not testPersistent :
    # Get the chroma client and set it to use duckdb+parquet (a normal db like sqlite3 and the parquet file format [which is column oriented])
    client = chromadb.Client()
else:
    # Get a chromadb persistent (data remains after the end of the execution) client
    client = chromadb.PersistentClient(path="./db")

# Create a collection (think of it like it's an sql table)
collection = client.get_or_create_collection(name="Students")

# # Add the data to the collection
# collection.add(
#     documents = [student_info, club_info, university_info],
#     metadatas = [{"source": "student info"},{"source": "club info"},{'source':'university info'}],
#     ids = ["id1", "id2", "id3"]
# )

results = collection.query(
    query_texts=["What is the university name?"],
    n_results=2
)

# print(results['ids'][0][0])
# print(results['metadatas'][0])
# print(results['documents'][0])

class ChromaQuery(BaseModel):
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
        # print(chromaResults['ids'][0][i])
        # print(chromaResults['metadatas'][0][i]['source'])
        # print(chromaResults['documents'][0][i])
        result = ChromaResult(id = chromaResults['ids'][0][i], source = chromaResults['metadatas'][0][i]['source'], info = chromaResults['documents'][0][i])
        results.append(result)
    
    return results

# append_result(results)
# print(append_result(results))
# Embedding(userPrompt="lll", resources=append_result(results) )


@app.post("/query/")
async def create_item(chromaQuery: ChromaQuery):
    print(chromaQuery.userPrompt)
    print(chromaQuery.n_results)

    results = collection.query(
        query_texts=["What is the university name?"],
        n_results=2
    )

    response = Embedding(userPrompt=chromaQuery.userPrompt, resources=append_result(results) )
    return response
