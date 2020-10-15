from typing import List, Union

import numpy as np
from pydantic import BaseModel

from database import get_comment_body, get_comment_embedding
from embedding import get_embedding_for_texts
from tools import unit_normalize

class Comment(BaseModel):
    id: int
    body: str

class SessionUpdateParams(BaseModel):
    id: int

class Session():
    def __init__(self):
        self.elements: List[ConceptElement] = []
    
    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, elements):
        self.__elements = elements

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

    def remove_element(self, param: SessionUpdateParams):
        del self.elements[param.id]


    def get_comments(self, index) -> List[Comment]:
        comment_ids = index.get_nearest_comment_ids(self.vector)
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
    body: str = ""

    def set_body(self):
        self.body = get_comment_body(self.id)

    def get_embedding(self):
        return get_comment_embedding(self.id)

ConceptElement = Union[SeedTextParams, CommentAnnotationParams]

