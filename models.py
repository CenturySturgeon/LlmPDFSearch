from pydantic import BaseModel
from typing import List

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

class ChromaCollection(BaseModel):
    name: str
    isPersistent: bool | None = False