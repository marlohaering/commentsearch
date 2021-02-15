from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')

def get_embedding_for_texts(texts: List[str]) -> np.ndarray:
	return model.encode(texts)
