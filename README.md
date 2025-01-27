# Sentiment Analysis on IMDB Dataset

## Dataset
Download the dataset from Kaggle: [IMDB Dataset of 50K Movie Reviews](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews).

---

## Steps to Set Up and Run the Project

### 1. Upload Data to MySQL
1. Open the `data_setup.py` file and replace the following fields with your MySQL credentials:
   ```python
   host="localhost",
   user="root",
   password="root",
   database="movie"
