import os
import re
import feedparser
import requests
import weaviate
from dotenv import load_dotenv
from html_parser import MyHTMLParser
import openai
from transformers import AutoTokenizer
import math

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')
openai.api_key = OPEN_AI_KEY
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")


def summarize(text):
    content_tokens = len(tokenizer.encode(text))
    max_tokens = 3097

    if content_tokens > max_tokens:
        parts_number = math.ceil(content_tokens / max_tokens)
        text = split_into_parts(text, parts_number)[0]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "system",
         "content": "Your task is to prepare a summary of a text provided by user. The summary is intended to be purely informative. Do not use suggestions, commands or prohibitions. The summary must fit within 280 characters."},
        {"role": "user",
         "content": "Provide me a summary of the following text: " + text}
    ])

    return response['choices'][0]['message']['content']

def split_into_parts(text, num_parts):
    # Split the text into sentences using regular expressions
    sentences = re.split(r'(?<=\w\.)\s+', text)

    # Calculate the number of sentences per part
    sentences_per_part = len(sentences) // num_parts

    # Initialize a list to store the parts
    parts = []

    # Loop through each part
    for i in range(num_parts):
        # Calculate the start and end indices for the current part
        start = i * sentences_per_part
        end = (i + 1) * sentences_per_part

        # Ensure that the end index falls at the end of a sentence
        while end < len(sentences) and not sentences[end].endswith('.'):
            end += 1

        # Add the sentences for the current part to the parts list
        part = ' '.join(sentences[start:end])
        parts.append(part)

    return parts


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

                try:
                    with client.batch as batch:
                        batch.batch_size = 100

                        for entry in feed:
                            parser = MyHTMLParser()
                            parser.feed(entry.content[0]['value'] if 'content' in entry else entry.summary)
                            parsed_content = parser.get_data()

                            properties = {
                                'title': entry.title,
                                'content': parsed_content,
                                'summary': summarize(parsed_content),
                                'link': entry.link
                            }

                            client.batch.add_data_object(properties, "FeedItem")

                except Exception as e:
                    print(e)

    print('Database feeded successfully!')


if __name__ == '__main__':
    feed_database()
