from collections import defaultdict
from typing import DefaultDict, Dict, List, Union

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from commentsearch.ann_index import CommentAnnIndex
from commentsearch.models import Session, Comment, SeedTextParams, CommentAnnotationParams, \
    ConceptElement, SessionUpdateParams

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

def create_response(session: Session) -> Dict[str, Union[List[ConceptElement], List[Comment]]]:
    return {
        'session': session.elements,
        'comments': session.get_comments(index)
        }

RequestRespone = Dict[str, Union[List[ConceptElement], List[Comment]]]

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
