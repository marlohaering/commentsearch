from typing import Union

import numpy as np
from pydantic import BaseModel

from commentsearch.database import get_comment_body, get_comment_embedding
from commentsearch.embedding import get_embedding_for_texts
from commentsearch.tools import unit_normalize


class Comment(BaseModel):
    id: int
    body: str


class SessionUpdateParams(BaseModel):
    id: int


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
