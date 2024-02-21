from flask import Flask, render_template, request
import requests
from textblob import TextBlob
from sumy.summarizers.lsa import LsaSummarizer                 
from sumy.parsers.plaintext import PlaintextParser                   
from sumy.nlp.tokenizers import Tokenizer 

import asyncio
import os
from pyppeteer import launch
from bs4 import BeautifulSoup
import csv 
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from scipy.special import softmax
# https://medium.com/mlearning-ai/tweets-sentiment-analysis-with-roberta-1f30cf4e1035

app = Flask(__name__)

# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

current_location = os.path.dirname(os.path.abspath(__file__))

summarization = pipeline("summarization")

def fetch_data():
    data = []
    summarytext = ""
    summarytext2 = ""
    summarizer_lsa = LsaSummarizer()                   
    with open('result1.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # blob = TextBlob(row["Review Text"])
            # sentiment = blob.sentiment
            # sentiment_confidence = sentiment.polarity
            encoded_tweet = tokenizer(row["Review Text"], return_tensors='pt',padding='max_length', truncation=True, max_length=512)
            # print(encoded_tweet)
            output = model(**encoded_tweet)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            # Negative 0.072049744
            # Neutral 0.8416957
            # Positive 0.08625448
            entry = {
                'name': row['Person Name'],
                'rating': row["Rating"],
                'date':row["Date"],
                'sentiment' : labels[scores.argmax()] ,
                # 'sentiment': 'Positive' if sentiment_confidence >= 0 else 'Negative',
                # 'sentiment_confidence': round(abs(sentiment_confidence), 2),
                'Scores' : " ".join(labels[i] + ":" + str(scores[i]) for i in range(3)),
                'comment': row["Review Text"],
            }
            summarytext +=  row["Review Text"]
            data.append(entry)
    data2 = []
    with open('result2.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # blob = TextBlob(row["Review Text"])
            # sentiment = blob.sentiment
            # sentiment_confidence = sentiment.polarity
            encoded_tweet = tokenizer(row["Review Text"], return_tensors='pt',padding='max_length', truncation=True, max_length=512)
            # print(encoded_tweet)
            output = model(**encoded_tweet)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            # Negative 0.072049744
            # Neutral 0.8416957
            # Positive 0.08625448
            entry = {
                'name': row['Person Name'],
                'rating': row["Rating"],
                'date':row["Date"],
                'sentiment' : labels[scores.argmax()] ,
                # 'sentiment': 'Positive' if sentiment_confidence >= 0 else 'Negative',
                # 'sentiment_confidence': round(abs(sentiment_confidence), 2),
                'Scores' :  {label: score for label, score in zip(labels, scores)}, 
                'comment': row["Review Text"],
            }
            summarytext +=  row["Review Text"]
            data2.append(entry)

    # summarizer_lsa(parser.document,2)
    parser1 = PlaintextParser.from_string(summarytext,Tokenizer("english")) 
    parser2 = PlaintextParser.from_string(summarytext2,Tokenizer("english")) 
    summary1 = "" 
    for sentence in summarizer_lsa(parser1.document,5):
        summary1+=str(sentence)
    summary2 =  ""
    for sentence in summarizer_lsa(parser2.document,5):
        summary2+=str(sentence)
    return data,data2,summary1,summary2

def summarize(original_text): 
    summary_text = summarization(original_text[:1024])[0]['summary_text']
    return summary_text

@app.route('/', methods=['GET', 'POST'])
def index():
    # data1,data2,summary1,summary2 = fetch_data()
    # with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     fieldnames = ['name', 'rating', 'date', 'sentiment', 'Scores', 'comment']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for entry in data1:
    #         writer.writerow(entry)

    # with open('data2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     fieldnames = ['name', 'rating', 'date', 'sentiment', 'Scores', 'comment']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for entry in data2:
    #         writer.writerow(entry)
    # with open("summary1.txt",'w') as txtfile:
    #     txtfile.write(summary1)
    # with open("summary2.txt",'w') as txtfile:
    #     txtfile.write(summary2)
    sentiment_distribution1 = {"Positive":0,"Negative":0,"Neutral":0}
    sentiment_distribution2 = {"Positive":0,"Negative":0,"Neutral":0}
    data1 = []
    data1_comments = ""
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data1.append(row)
            data1_comments += row["comment"]
            sentiment_distribution1[row['sentiment']]+=1
    data2 = []
    data2_comments = ""
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data2.append(row)
            data2_comments += row["comment"]
            sentiment_distribution2[row['sentiment']]+=1
    
    with open("summary1.txt",'r') as txtfile:
        summary1 = txtfile.read()
    
    with open("summary2.txt",'r') as txtfile:
        summary2 = txtfile.read()
    # summary1 = summarize(data1_comments)
    # summary2 = summarize(data2_comments)
    return render_template('index.html', data1 = data1, data2 = data2, sentiment_distribution1 = sentiment_distribution1, sentiment_distribution2 = sentiment_distribution2, summary1 = summary1,summary2 = summary2)

if __name__ == '__main__':
    app.run(debug=True)
