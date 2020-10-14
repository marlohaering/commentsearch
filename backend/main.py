from typing import Optional, DefaultDict, List, Union
from dataclasses import dataclass
from functools import lru_cache, cached_property
import numpy as np
from database import get_comment_embedding, get_comment_body
from embedding import get_embedding_for_texts
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from collections import defaultdict
from ann_index import CommentAnnIndex
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


index = CommentAnnIndex()

def unit_normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)

class Session:
    def __init__(self):
        self.elements: List[ConceptElement] = []
    
    @property
    def vector(self) -> np.ndarray:
        vector = np.zeros(768)
        for element in self.elements:
            emb = unit_normalize(element.get_embedding())
            if element.positive:
                vector += emb
            else:
                vector += vector - emb
            vector = unit_normalize(vector)
        return vector

sessions: DefaultDict[str, Session] = defaultdict(Session)

def get_session(session_id: str) -> Session:
    return sessions[session_id]


class Comment(BaseModel):
    id: int
    body: str


def get_comments_for_session(session : Session) -> List[Comment]:
    comment_ids = index.get_nearest_comment_ids(session.vector)
    comment_bodies = [get_comment_body(cid.item()) for cid in comment_ids]

    return [Comment(id=id, body=body) for id, body in zip(comment_ids, comment_bodies)]

class SeedTextParams(BaseModel):
    text: str
    positive: bool = True

    def get_embedding(self):
        print('Computing embedding', self.text)
        return get_embedding_for_texts([self.text])[0]


class CommentAnnotationParams(BaseModel):
    id: int
    positive: bool

    def get_embedding(self):
        return get_comment_embedding(self.id)

ConceptElement = Union[SeedTextParams, CommentAnnotationParams]

@app.post("/{session_id}/texts", response_model=List[Comment])
def post_seed_text(params: SeedTextParams, session = Depends(get_session)):
    session.elements.append(params)
    return get_comments_for_session(session)


@app.post("/{session_id}/comments", response_model=List[Comment])
def post_comment_annotation(params: CommentAnnotationParams, session = Depends(get_session)):
    session.elements.append(params)
    return get_comments_for_session(session)


# pip install torch torchvision transformers sentence-transformers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8081)
