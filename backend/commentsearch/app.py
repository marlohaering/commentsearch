from collections import defaultdict
from typing import DefaultDict, Dict, List, Union

import numpy as np
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from commentsearch.ann_index import CommentAnnIndex
from commentsearch.concept_vector_calculations import calculate_moving_vector
from commentsearch.database import get_comment_body, get_random_comments
from commentsearch.models import (Comment, CommentAnnotationParams, ConceptElement,
                                  SeedTextParams, SessionUpdateParams, CoLiBertLinkParams)
from commentsearch.session import Session
from commentsearch.colibert import TextPairClassificationModel, get_colibert

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


# CoLiBERT

@app.post("/colibert/link", response_model=List[str])
def post_colibert_link_comments(
        params: CoLiBertLinkParams,
        limit: int = 20,
        samples: int = 500,
        colibert: TextPairClassificationModel = Depends(get_colibert),
):
    random_comments = get_random_comments(count=samples)
    comment_bodies = [body for _, body in random_comments]
    scores = colibert.get_pairwise_scores(texts_a=[params.query], texts_b=comment_bodies)
    comment_order = np.argsort(scores)[0, :-limit-1:-1]
    return [comment_bodies[idx] for idx in comment_order]
