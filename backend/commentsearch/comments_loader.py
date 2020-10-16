import csv
from itertools import islice
from typing import Iterable

import requests
from pymongo import MongoClient
from tqdm import tqdm

from commentsearch.config import COMMENTS_FILE

"""Create the comments.csv for initialization"""


def generate_comments_file(comments: Iterable[str]):
    with COMMENTS_FILE.open('w+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for comment in tqdm(comments):
            writer.writerow((comment,))


def fetch_comments_from_mongo() -> Iterable[str]:
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


def fetch_reviews_from_play_store(app_id: str, num: int) -> Iterable[str]:
    query = (
        'query fetchReviews($appId: String!, $num: Int!) {'
        '  app(appId: $appId) {'
        '    reviews(num: $num, sort: HELPFULNESS) {'
        '      text'
        '    }'
        '  }'
        '}'
    )
    response = requests.post('http://localhost:4000/', json={
        'query': query,
        'variables': {'appId': app_id, 'num': num},
    })

    if not 200 <= response.status_code < 300:
        raise Exception(
            f'Could not query the PlayStore GraphQL API. '
            f'Please make sure that it is running on port 4000. '
            f'Use "docker run --rm -p 4000:4000 ietz/google-play-graphql-api" to start it. '
            f'Got the following {response.status_code} response: "{response.text}".'
        )

    return [review['text'] for review in response.json()['data']['app']['reviews']]


if __name__ == '__main__':
    generate_comments_file(fetch_reviews_from_play_store('com.whatsapp', 10_000))
    # generate_comments_file(islice(fetch_comments_from_mongo(), 100_000))
