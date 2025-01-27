import mysql.connector
import pandas as pd

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="movie"
)

df = pd.read_csv('data.csv')
cursor = db.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    review TEXT,
    sentiment VARCHAR(10)
)
"""
cursor.execute(create_table_query)

insert_query = "INSERT INTO reviews (review, sentiment) VALUES (%s, %s)"
for index, row in df.iterrows():
    cursor.execute(insert_query, (row['review'], row['sentiment']))

db.commit()

cursor.close()
db.close()
