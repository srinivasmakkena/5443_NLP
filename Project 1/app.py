from flask import Flask, render_template, request
import requests
from textblob import TextBlob

import asyncio
import os
from pyppeteer import launch
from bs4 import BeautifulSoup
import csv 
app = Flask(__name__)

current_location = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET', 'POST'])
def index():
    data = fetch_data()
    return render_template('index.html', data=data)

def fetch_data():
    data = []
    # with open("result.csv",'r', encoding="utf-8",) as f:
    #     content = f.readlines()[1:]
    #     print(content[1].split(","))
    with open('result.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            blob = TextBlob(row["Review Text"])
            sentiment = blob.sentiment
            sentiment_confidence = sentiment.polarity

            entry = {
                'name': row['Person Name'],
                'rating': row["Rating"],
                'date':row["Date"],
                'sentiment': 'Positive' if sentiment_confidence >= 0 else 'Negative',
                'sentiment_confidence': round(abs(sentiment_confidence), 2),
                'comment': row["Review Text"],
            }
    
            data.append(entry)

    return data

if __name__ == '__main__':
    app.run(debug=True)
