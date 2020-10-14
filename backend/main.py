from typing import Optional, DefaultDict, List
from dataclasses import dataclass
from functools import lru_cache, cached_property
import numpy as np
from embedding import get_embedding_for_texts
import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from collections import defaultdict


app = FastAPI()

class Session:
    def __init__(self):
        self.elements: List[ConceptElement] = []
    
    @property
    def vector(self) -> np.ndarray:
        return np.sum([e.embedding for e in self.elements], axis=0)


sessions: DefaultDict[str, Session] = defaultdict(Session)

def get_session(session_id: str) -> Session:
    return sessions[session_id]


class ConceptElement(BaseModel):
    pass

    @property
    def embedding(self):
        raise NotImplementedError()

class SeedTextParams(ConceptElement):
    text: str

    @cached_property
    def embedding(self):
        return get_embedding_for_texts([self.text])[0]


class CommentAnnotationParams(ConceptElement):
    id: int
    positive: bool

    @property
    def parity(self) -> int:
        return +1 if self.positive else -1

    @property
    def embedding(self):
        return self.parity * get_comment_embedding(self.id)


@app.post("/{session_id}/texts")
def post_seed_text(params: SeedTextParams, session = Depends(get_session)):
    session.elements.append(params)
    print(session)
    return 200


@app.post("/{session_id}/comments")
def post_comment_annotation(params: CommentAnnotationParams, session = Depends(get_session)):
    session.elements.append(params)
    print(session)
    return 200


# pip install torch torchvision transformers sentence-transformers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8081, reload=True)
