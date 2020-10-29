import itertools
import math
import time

import hnswlib
import numpy as np
from sklearn.neighbors import NearestNeighbors

from commentsearch.config import INDEX_FILE
from commentsearch.database import get_comment_embeddings, get_comment_body, get_comment_embedding


class CommentAnnIndex:
    def __init__(self, space='cosine'):
        save_file = INDEX_FILE(space)
        dim = 768
        self.p = hnswlib.Index(space, dim=dim)

        if save_file.exists():
            self.p.load_index(str(save_file), max_elements=0)
        else:
            print('Building index')

            ids, embeddings = list(zip(*get_comment_embeddings()))
            data = np.array(embeddings)
            num_elements, dim = data.shape
            self.p.init_index(max_elements=num_elements,
                              ef_construction=200, M=16)
            self.p.add_items(data, ids)
            self.p.set_ef(50)  # should always be > k, determines recall
            self.p.save_index(str(save_file))

            print('Evaluating index')
            evaluate_hnsw_index(self.p, data, max_k=49, num_sample_queries=1000)

    def get_nearest_comment_ids(self, embedding: np.ndarray, k: int = 49) -> np.ndarray:
        labels, distances = self.p.knn_query(embedding, k=k)
        return labels[0]


def evaluate_hnsw_index(p: hnswlib.Index, data: np.ndarray, max_k: int, num_sample_queries: int):
    m, dim = data.shape
    sample_vectors = np.random.uniform(low=-1.0, high=1.0, size=(num_sample_queries, dim))

    exact_knn = NearestNeighbors(n_neighbors=50, metric='cosine')
    exact_knn.fit(data)
    Y_true = 1 + exact_knn.kneighbors(sample_vectors, n_neighbors=100, return_distance=False)

    test_ks = [(10**f)*p for f, p in itertools.product(range(math.ceil(math.log10(max_k))), [1, 2, 5]) if (10**f)*p <= max_k]
    test_ks += [max_k]
    for k in test_ks:
        found = 0
        for sample_vector, y_true in zip(sample_vectors, Y_true):
            y_pred, _ = p.knn_query(sample_vector, k=k)
            found += sum(y in y_pred for y in y_true[:k])

        recall = found / k / num_sample_queries
        print(f'Recall for k={k}: {recall:.01%}')


if __name__ == "__main__":
    start = time.time()
    index = CommentAnnIndex()
    print(f'Index creation took {time.time() - start:.01f}s')

    random_id = 100
    random_embedding = get_comment_embedding(random_id)
    start = time.time()
    nearest = index.get_nearest_comment_ids(random_embedding, 5)
    print(f'Neighbour selection took {time.time() - start:.01f}s')

    random_body = get_comment_body(random_id)
    print(f"seed comment: {random_body}")
    print()

    for i, cid in enumerate(nearest):
        body = get_comment_body(cid.item())
        print(f'{i+1:02d}. comment [{cid:06d}]: "{body}"')
        print()
