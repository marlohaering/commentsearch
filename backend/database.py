import csv

import psycopg2
from psycopg2.extras import execute_values
from more_itertools import chunked
from tqdm import tqdm

from config import COMMENTS_FILE


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
        "CREATE TABLE documents ("
        "   id bigserial primary key,"
        "   body text not null"
        ")"
    )


@with_connection
def init_data(conn):
    cur = conn.cursor()

    with COMMENTS_FILE.open('r', encoding='utf-8') as f:
        for comment_batch in chunked(tqdm(csv.reader(f)), n=500):
            execute_values(cur, "INSERT INTO documents (body) VALUES %s", comment_batch)


if __name__ == '__main__':
    main()
