import os

import feedparser
import requests
import weaviate
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')

def get_source(url):
    try:
        return feedparser.parse(url)

    except requests.exceptions.RequestException as e:
        print(e)


def get_feed(url):
    return get_source(url)['entries']


def run():
    rss_url = [
        'https://www.reutersagency.com/feed/?best-regions=middle-east&post_type=best',
        'https://www.crisisgroup.org/rss'
    ]
    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={
            "X-OpenAI-Api-Key": OPEN_AI_KEY
        }
    )

    client.schema.delete_class("FeedItem")

    class_obj = {
        "class": "FeedItem",
        "vectorizer": "text2vec-openai"
    }
    client.schema.create_class(class_obj)

    feed = get_feed(rss_url)

    with client.batch as batch:
        batch.batch_size = 100

        for entry in feed:
            print({
                'title': entry.title,
                'published': entry.published,
                'summary': entry.summary,
                'content': entry.content[0]['value']
            })

            properties = {
                'title': entry.title,
                'published': entry.published,
                'summary': entry.summary,
                'content': entry.content[0]['value']
            }
            client.batch.add_data_object(properties, "FeedItem")


if __name__ == '__main__':
    run()
