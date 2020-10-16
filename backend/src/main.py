from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property, lru_cache
from typing import DefaultDict, Dict, List, Optional, Union

import numpy as np
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ann_index import CommentAnnIndex
from concept_vector_calculations import calculate_moving_vector
from database import get_comment_body
from models import (Comment, CommentAnnotationParams, ConceptElement,
                    SeedTextParams, SessionUpdateParams)
from session import Session

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


index = CommentAnnIndex()

sessions: DefaultDict[str, Session] = defaultdict(Session)

def get_session(session_id: str) -> Session:
    return sessions[session_id]

def get_nearest_comments(vector: np.ndarray, index) -> List[Comment]:
    comment_ids = index.get_nearest_comment_ids(vector)
    comment_bodies = [get_comment_body(cid.item()) for cid in comment_ids]
    return [Comment(id=id, body=body) for id, body in zip(comment_ids, comment_bodies)]

RequestRespone = Dict[str, Union[List[ConceptElement], List[Comment]]]


def create_response(session: Session) -> RequestRespone:
    concept_vector = calculate_moving_vector(session.elements)
    comments = get_nearest_comments(concept_vector, index)
    return {
        'session': session.elements,
        'comments': comments
        }


@app.post("/{session_id}/texts", response_model=RequestRespone)
def post_seed_text(params: SeedTextParams, session: Session = Depends(get_session)):
    session.elements.append(params)
    return create_response(session)


@app.post("/{session_id}/comments", response_model=RequestRespone)
def post_comment_annotation(params: CommentAnnotationParams, session: Session = Depends(get_session)):
    params.set_body()
    session.elements.append(params)
    return create_response(session)

@app.put("/{session_id}/update", response_model=RequestRespone)
def put_update_session(params: SessionUpdateParams, session: Session = Depends(get_session)):
    session.remove_element(params)
    return create_response(session)

# pip install torch torchvision transformers sentence-transformers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8081)
