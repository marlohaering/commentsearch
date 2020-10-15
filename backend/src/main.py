from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property, lru_cache
from typing import DefaultDict, List, Optional

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ann_index import CommentAnnIndex
from models import Session, Comment, SeedTextParams, CommentAnnotationParams

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


@app.post("/{session_id}/texts", response_model=List[Comment])
def post_seed_text(params: SeedTextParams, session: Session = Depends(get_session)) -> List[Comment]:
    session.elements.append(params)
    return session.get_comments(index)


@app.post("/{session_id}/comments", response_model=List[Comment])
def post_comment_annotation(params: CommentAnnotationParams, session: Session = Depends(get_session)) -> List[Comment]:
    session.elements.append(params)
    return session.get_comments(index)


# pip install torch torchvision transformers sentence-transformers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8081)
