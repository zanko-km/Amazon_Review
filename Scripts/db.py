import psycopg2

# اطلاعات اتصال به پایگاه‌داده
DB_NAME = "Phase_2"
DB_USER = "postgres"
DB_PASSWORD = 'pass'
DB_HOST = "localhost"
DB_PORT = "5432"

# اتصال به پایگاه داده
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# ایجاد جدول users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT
);
""")

# ایجاد جدول products
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY
);
""")

# ایجاد جدول reviews با کلیدهای خارجی
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id),
    product_id TEXT REFERENCES products(product_id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    summary TEXT,
    review_text TEXT,
    review_date DATE
);
""")

# ذخیره تغییرات و بستن اتصال
conn.commit()
cursor.close()
conn.close()

print("✅ Data Base created successfully!")
