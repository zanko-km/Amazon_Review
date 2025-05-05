import pandas as pd
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from textblob import TextBlob
import json

# SQLAlchemy (connecting to db)
engine = create_engine("postgresql+psycopg2://postgres:pass@localhost:5432/Phase_2")

#  reading reviews table in db
query = "SELECT * FROM reviews;"
df = pd.read_sql(query, engine)

# embedding model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
df['review_embedding'] = model.encode(df['review_text'].tolist()).tolist()
df['summary_embedding'] = model.encode(df['summary'].tolist()).tolist()

# date
df['day_of_week'] = pd.to_datetime(df['review_date'], errors='coerce').dt.day_name()

# (Sentiment)
def classify_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity if text else 0
    return 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'

df['review_sentiment'] = df['review_text'].fillna('').apply(classify_sentiment)
df['summary_sentiment'] = df['summary'].fillna('').apply(classify_sentiment)

# length
def count_unique_chars(text): return len(set(text)) if isinstance(text, str) else 0
def count_words(text): return len(text.split()) if isinstance(text, str) else 0
def count_chars(text): return len(text) if isinstance(text, str) else 0

df['review_unique_chars'] = df['review_text'].apply(count_unique_chars)
df['review_word_count'] = df['review_text'].apply(count_words)
df['review_char_count'] = df['review_text'].apply(count_chars)
df['summary_unique_chars'] = df['summary'].apply(count_unique_chars)
df['summary_word_count'] = df['summary'].apply(count_words)
df['summary_char_count'] = df['summary'].apply(count_chars)


# creating new table if there is nothing
with engine.connect() as conn:
    conn.execute(text("""
       CREATE TABLE IF NOT EXISTS full_review_features (
            review_id SERIAL PRIMARY KEY,
            review_embedding FLOAT8[],
            summary_embedding FLOAT8[],
            day_of_week TEXT,
            review_sentiment TEXT,
            summary_sentiment TEXT,
            review_unique_chars INTEGER,
            review_word_count INTEGER,
            review_char_count INTEGER,
            summary_unique_chars INTEGER,
            summary_word_count INTEGER,
            summary_char_count INTEGER,
            FOREIGN KEY (review_id) REFERENCES reviews(review_id)
        );

    """))
    conn.commit()

# using jason instead of list
insert_query = text("""
    INSERT INTO full_review_features (
        review_id,
        review_embedding,
        summary_embedding,
        day_of_week,
        review_sentiment,
        summary_sentiment,
        review_unique_chars,
        review_word_count,
        review_char_count,
        summary_unique_chars,
        summary_word_count,
        summary_char_count
    )
    VALUES (
        :review_id, :review_embedding, :summary_embedding, :day_of_week,
        :review_sentiment, :summary_sentiment,
        :review_unique_chars, :review_word_count, :review_char_count,
        :summary_unique_chars, :summary_word_count, :summary_char_count
    )
""")


records = []
for _, row in df.iterrows():
    record = {
        'review_id': int(row['review_id']),
        'review_embedding': row['review_embedding'],
        'summary_embedding': row['summary_embedding'],
        'day_of_week': row['day_of_week'],
        'review_sentiment': row['review_sentiment'],
        'summary_sentiment': row['summary_sentiment'],
        'review_unique_chars': int(row['review_unique_chars']),
        'review_word_count': int(row['review_word_count']),
        'review_char_count': int(row['review_char_count']),
        'summary_unique_chars': int(row['summary_unique_chars']),
        'summary_word_count': int(row['summary_word_count']),
        'summary_char_count': int(row['summary_char_count'])
    }
    records.append(record)

# writing in db
with engine.begin() as conn:
    for rec in records:
        conn.execute(insert_query, rec)

print("✅ Data inserted into 'full_review_features' successfully.")
