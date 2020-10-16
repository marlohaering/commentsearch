import csv
import pickle
from functools import lru_cache
from typing import List, Tuple

import numpy as np
import psycopg2
from more_itertools import chunked, collapse
from psycopg2.extras import execute_values
from tqdm import tqdm

from commentsearch.config import COMMENTS_FILE
from commentsearch.embedding import get_embedding_for_texts


def db_connect():
    return psycopg2.connect(host='localhost', port=5432, dbname='search', user='postgres', password='pw')


def with_connection(fn):
    def with_connection_inner(*args, **kwargs):
        conn = db_connect()
        try:
            result = fn(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return result

    return with_connection_inner


def main():
    init_schema()
    init_data()


@with_connection
def init_schema(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS documents")
    cur.execute(
        "CREATE TABLE documents ( "
        "   id bigserial primary key, "
        "   body text not null, "
        "   embedding BYTEA not null"
        ")"
    )


@with_connection
def init_data(conn):
    cur = conn.cursor()

    with COMMENTS_FILE.open('r', encoding='utf-8') as f:
        for body_batch in chunked(tqdm(collapse(csv.reader(f))), n=500):
            embedding_batch = get_embedding_for_texts(body_batch)
            execute_values(cur, "INSERT INTO documents (body, embedding) VALUES %s", zip(
                body_batch, [pickle.dumps(e) for e in embedding_batch]))


@lru_cache
@with_connection
def get_comment_embedding(conn, id: int) -> np.ndarray:
    print(f'Looking up embedding from db for {id}')
    cur = conn.cursor()
    cur.execute("SELECT embedding FROM documents WHERE id = %s", (id,))
    return pickle.loads(cur.fetchone()[0])


@with_connection
def get_comment_body(conn, id: int) -> str:
    cur = conn.cursor()
    cur.execute("SELECT body FROM documents WHERE id = %s", (id,))
    return cur.fetchone()[0]


@with_connection
def get_comment_embeddings(conn) -> List[Tuple[int, np.ndarray]]:
    cur = conn.cursor()
    cur.execute("SELECT id, embedding FROM documents")
    result = cur.fetchall()
    return [(id, pickle.loads(emb)) for id, emb in result]


if __name__ == '__main__':
    main()
    # emb = get_comment_embeddings()
    # print(emb[:2])
