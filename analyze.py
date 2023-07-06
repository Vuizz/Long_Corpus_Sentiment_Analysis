import spacy
from spacy import displacy
from spacy.pipeline import Sentencizer
import pandas as pd

from prettytable import PrettyTable

import os

nlp = spacy.load("en_core_web_sm")

def analyze_text(text):

    doc = nlp(text)

    # Analyze syntax
    nouns = [chunk.text for chunk in doc.noun_chunks]  # Noun phrases
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]  # Verbs

    for entity in doc.ents:
        print(f"{entity.text} ({entity.label_})")

    # for token1 in doc:
    #     for token2 in doc:
    #         print(token1.text, token2.text, token1.similarity(token2))

    sentiment = doc.sentiment
    print(f'Sentiment: {sentiment}')

df = pd.read_csv('stock_news.csv')

last_row = df.iloc[-4]
table = PrettyTable()
table.field_names = ['Ticker', 'Title']
table.add_row([last_row['ticker'], last_row['title']])
print(table)
article = last_row['article']
with open(article, 'r') as f:
    text = f.read()
    analyze_text(text)