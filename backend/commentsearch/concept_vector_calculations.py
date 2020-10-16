import numpy as np
from commentsearch.tools import unit_normalize
from typing import List
from commentsearch.models import ConceptElement


def calculate_moving_vector(elements: List[ConceptElement]) -> np.ndarray:
    vector = np.zeros(768)
    for element in elements:
        emb = unit_normalize(element.get_embedding())
        if element.positive:
            vector += emb
        else:
            vector += vector - emb
        vector = unit_normalize(vector)
    return vector