from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import joblib
import torch
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

app = Flask(__name__)

logistic_model = joblib.load('sentiment_model.joblib')
distilbert_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
distilbert_tokenizer = AutoTokenizer.from_pretrained(distilbert_model_name)
distilbert_model = AutoModelForSequenceClassification.from_pretrained(distilbert_model_name)

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text_tokens = text.split()
    text = ' '.join([word for word in text_tokens if word not in stop_words])
    return text

def preprocess_text_distilbert(text):
    return distilbert_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_sentiment():
    try:
        data = request.get_json()
        review_text = data.get('review_text', None)
        model_choice = data.get('model', 'logistic_regression')  

        if not review_text:
            return jsonify({'error': 'No review text provided'}), 400

        if model_choice == 'logistic_regression':
            processed_text = preprocess_text(review_text)
            prediction = logistic_model.predict([processed_text])
            sentiment = "positive" if prediction[0] == 1 else "negative"

        elif model_choice == 'distilbert':
            inputs = preprocess_text_distilbert(review_text)
            with torch.no_grad():
                outputs = distilbert_model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(scores).item()
            sentiment = "positive" if predicted_class == 1 else "negative"

        else:
            return jsonify({'error': 'Invalid model choice'}), 400

        return jsonify({'sentiment_prediction': sentiment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
