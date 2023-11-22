from pydantic import BaseModel
from typing import List

class ChromaPrompt(BaseModel):
    userPrompt: str
    collectionName: str
    isPersistent: bool | None = False
    n_results: int | None = 1

class ChromaResult(BaseModel):
    id: str
    source: str
    info: str
    
class InContextResponse(BaseModel):
    userPrompt: str
    resources: List

class ChromaCollection(BaseModel):
    name: str
    isPersistent: bool | None = False

class MetaDatas(BaseModel):
    source: str

class ChromaDocument(BaseModel):
    collection: str
    ids: List[str]
    bodies: List[str]
    metadatas: List[MetaDatas]
    
