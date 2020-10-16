import csv
from itertools import islice

from tqdm import tqdm
from pymongo import MongoClient

from commentsearch.config import COMMENTS_FILE

"""Create the comments.csv for initialization"""


def generate_comments_file():
    with COMMENTS_FILE.open('w+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        num = 100_000
        for comment in tqdm(islice(fetch_root_comments_from_mongo(), num), total=num):
            writer.writerow((comment,))


def fetch_root_comments_from_mongo():
    client = MongoClient('localhost', 27017)
    comments = client['spon']['threads'].aggregate([
        { '$unwind': { 'path': '$posts' } },
        { '$match': { 'posts.body.0.type': { '$eq': 'content' } } },
        { '$project': { '_id': 0, 'title': '$posts.title', 'body': { '$arrayElemAt': [ '$posts.body.text', 0 ] } } }
    ])

    for comment in comments:
        title, body = comment['title'], comment['body']
        if not body:
            continue

        if body[0].islower() and title:
            yield f'{title} {body}'
        else:
            yield body


if __name__ == '__main__':
    generate_comments_file()
