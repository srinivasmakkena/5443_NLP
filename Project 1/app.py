from flask import Flask, render_template, request
import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from scipy.special import softmax
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

app = Flask(__name__)

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)
labels = ['Negative', 'Neutral', 'Positive']

summarization = pipeline("summarization")

def analyze_sentiment(review_text):
    encoded_tweet = tokenizer(review_text, return_tensors='pt', padding='max_length', truncation=True, max_length=512)
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    sentiment = labels[scores.argmax()]
    return sentiment, scores

def fetch_data(file_path):
    data = []
    summary_text = ""
    summarizer_lsa = LsaSummarizer()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sentiment, scores = analyze_sentiment(row["Review Text"])
            entry = {
                'name': row['Person Name'],
                'rating': row["Rating"],
                'date': row["Date"],
                'sentiment': sentiment,
                'Scores': {label: score for label, score in zip(labels, scores)},
                'comment': row["Review Text"],
            }
            summary_text += row["Review Text"]
            data.append(entry)

    parser = PlaintextParser.from_string(summary_text, Tokenizer("english"))
    summary = ""
    for sentence in summarizer_lsa(parser.document, 5):
        summary += str(sentence)

    return data, summary
def write2csv(data1,data2,summary1,summary2):
    with open('data1.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'rating', 'date', 'sentiment', 'Scores', 'comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data1:
            writer.writerow(entry)

    with open('data2.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'rating', 'date', 'sentiment', 'Scores', 'comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data2:
            writer.writerow(entry)
    with open("summary1.txt",'w') as txtfile:
        txtfile.write(summary1)
    with open("summary2.txt",'w') as txtfile:
        txtfile.write(summary2)
def readfromcsv():
    data1 = []
    with open('data1.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data1.append(row)
    data2 = []
    with open('data2.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data2.append(row)
    
    with open("summary1.txt",'r') as txtfile:
        summary1 = txtfile.read()
    
    with open("summary2.txt",'r') as txtfile:
        summary2 = txtfile.read()
    return data1,data2,summary1,summary2
@app.route('/', methods=['GET', 'POST'])
def index():
    # data1, summary1 = fetch_data('result1.csv')
    # data2, summary2 = fetch_data('result2.csv')
    # write2csv(data1,data2,summary1,summary2)
    data1,data2,summary1,summary2 = readfromcsv()
    sentiment_distribution1 = get_sentiment_distribution(data1)
    sentiment_distribution2 = get_sentiment_distribution(data2)
    return render_template('index.html', data1=data1, data2=data2, 
                           sentiment_distribution1=sentiment_distribution1, 
                           sentiment_distribution2=sentiment_distribution2, 
                           summary1=summary1, summary2=summary2)

def get_sentiment_distribution(data):
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for entry in data:
        sentiment_distribution[entry['sentiment']] += 1
    return sentiment_distribution

if __name__ == '__main__':
    app.run(debug=True)
