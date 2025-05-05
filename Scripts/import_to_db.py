import pandas as pd
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname="Phase_2",
    user="postgres",
    password="pass",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# خواندن فایل CSV
df = pd.read_csv("Scripts/Dataset_cleaned.csv")

# تبدیل داده‌ها و درج در جداول
for index, row in df.iterrows():
    # اضافه کردن کاربر (اگر وجود نداشته باشه)
    cursor.execute("""
        INSERT INTO users (user_id, username)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """, (row['reviewerID'], row['reviewerName']))
    # اضافه کردن محصول (اگر وجود نداشته باشه)
    cursor.execute("""
        INSERT INTO products (product_id)
        VALUES (%s)
        ON CONFLICT (product_id) DO NOTHING;
    """, (str(row['asin']),))  # ← کاما یادت نره


    # اضافه کردن نظر
    cursor.execute("""
        INSERT INTO reviews (
            user_id, product_id, rating,
            summary, review_text, review_date
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        row['reviewerID'],
        str(row['asin']),
        int(row['overall']),
        row['cleaned_summary'],
        row['cleaned_review'],
        pd.to_datetime(row['reviewTime']).date(),
    ))

# ذخیره و بستن اتصال
conn.commit()
cursor.close()
conn.close()

print("✅ Confirmed!")
