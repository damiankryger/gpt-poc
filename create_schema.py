import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')


def create_schema():
    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={
            "X-OpenAI-Api-Key": OPEN_AI_KEY
        }
    )

    try:
        client.schema.get('FeedItem')

        print('Schema already exists. Skipping...')

    except weaviate.exceptions.UnexpectedStatusCodeException:
        class_obj = {
            "class": "FeedItem",
            "vectorizer": "text2vec-openai"
        }
        client.schema.create_class(class_obj)

        print('Schema created successfully!')


if __name__ == '__main__':
    create_schema()
