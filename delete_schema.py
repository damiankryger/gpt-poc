import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')


def delete_schema():
    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={
            "X-OpenAI-Api-Key": OPEN_AI_KEY
        }
    )

    try:
        client.schema.delete_class('FeedItem')

        print('Schema deleted successfully!')

    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        print(e)


if __name__ == '__main__':
    delete_schema()
