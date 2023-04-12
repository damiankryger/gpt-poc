import os

import feedparser
import requests
import weaviate
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')

def get_source(content):
    try:
        return feedparser.parse(content)

    except requests.exceptions.RequestException as e:
        print(e)

def get_feed(content):
    return get_source(content)['entries']

def feed_database():
    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={
            "X-OpenAI-Api-Key": OPEN_AI_KEY
        }
    )

    directory = 'feeds'
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            with open(os.path.join(directory, filename), 'r') as file:
                content = file.read()

                feed = get_feed(content)

                with client.batch as batch:
                    batch.batch_size = 100

                    for entry in feed:
                        try:
                            properties = {
                                'title': entry.title,
                                'published': entry.published,
                                'summary': entry.summary,
                                'content': entry.content[0]['value'] if 'content' in entry else ''
                            }

                            client.batch.add_data_object(properties, "FeedItem")

                        except AttributeError as e:
                            print(e)

    print('Database feeded successfully!')


if __name__ == '__main__':
    feed_database()