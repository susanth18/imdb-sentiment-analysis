import requests

url = 'http://127.0.0.1:5000/predict'

# Example input for Logistic Regression
data_lr = {'review_text': 'That surely is not an awful movie', 'model': 'logistic_regression'}
response_lr = requests.post(url, json=data_lr)
print(response_lr.json())

# Example input for DistilBERT
data_bert = {'review_text': 'That surely is not an awful movie', 'model': 'distilbert'}
response_bert = requests.post(url, json=data_bert)
print(response_bert.json())
