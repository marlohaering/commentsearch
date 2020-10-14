import csv
import pickle

import numpy as np
import psycopg2
from more_itertools import chunked, collapse
from psycopg2.extras import execute_values
from tqdm import tqdm

from config import COMMENTS_FILE
from embedding import get_embedding_for_texts


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
        for body_batch in chunked(tqdm(collapse(csv.reader(f))), n=10):
            embedding_batch = get_embedding_for_texts(body_batch)
            for body, embedding in zip(body_batch, embedding_batch):
                print(body, embedding)
                cur.execute("INSERT INTO documents (body, embedding) VALUES (%s, %s)", (body, pickle.dumps(embedding)))

@with_connection
def get_comment_embedding(conn, id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM documents WHERE id = %s", (id,))
    return cur.fetchone()

if __name__ == '__main__':
    main()
