import time

import hnswlib
import numpy as np

from commentsearch.config import INDEX_FILE
from commentsearch.database import get_comment_embeddings, get_comment_body, get_comment_embedding


class CommentAnnIndex():
    def __init__(self, space='cosine'):
        save_file = INDEX_FILE(space)
        dim = 768
        self.p = hnswlib.Index(space, dim = dim)

        if save_file.exists():
            self.p.load_index(str(save_file), max_elements = 0)
        else:
            ids, embeddings = list(zip(*get_comment_embeddings()))
            data = np.array(embeddings)
            num_elements, dim = data.shape
            self.p.init_index(max_elements = num_elements, ef_construction = 200, M = 16)
            self.p.add_items(data, ids)
            self.p.set_ef(50) # should always be > k, determines recall
            self.p.save_index(str(save_file))


    def get_nearest_comment_ids(self, embedding: np.ndarray, k: int = 10) -> np.ndarray:
        labels, distances = self.p.knn_query(embedding, k = k)
        return labels[0]




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
