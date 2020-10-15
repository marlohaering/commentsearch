from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('xlm-r-bert-base-nli-stsb-mean-tokens')

def get_embedding_for_texts(texts: List[str]) -> np.ndarray:
	return model.encode(texts)