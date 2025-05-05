import psycopg2

# اتصال به پایگاه داده
conn = psycopg2.connect(
    dbname="Phase_2",
    user="postgres",
    password="pass",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("SELECT product_id, COUNT(*) AS number_of_reviews FROM reviews WHERE product_id = 'B00004Y2UT' GROUP BY product_id;")
reviews = cursor.fetchall()
print("\nNumber of reviews for product with id = B00004Y2UT :")
for review in reviews:
    print(review)

# برای دریافت ۵ داده اول از جدول products
cursor.execute("SELECT product_id, AVG(rating) AS avg_rating FROM reviews GROUP BY product_id ORDER BY avg_rating DESC LIMIT 10;")
products = cursor.fetchall()
print("Top 10 products based on overall:")
for product in products:
    print(product)

# برای دریافت ۵ داده اول از جدول reviews
cursor.execute("SELECT AVG(rating) AS average_rating FROM reviews;")
reviews = cursor.fetchall()
print("\nAverage of all overall:")
for review in reviews:
    print(review)

cursor.execute("SELECT p.product_id, COUNT(r.review_id) AS number_of_positive_reviews FROM products p JOIN reviews r ON p.product_id = r.product_id WHERE r.rating > 4 GROUP BY p.product_id ORDER BY number_of_positive_reviews DESC LIMIT 10;")
reviews = cursor.fetchall()
print("\nProducts with most high overall(>4):")
for review in reviews:
    print(review)

cursor.execute("SELECT u.username, r.user_id, COUNT(r.review_id) AS number_of_reviews, SUM(r.rating) AS total_rating FROM reviews r JOIN users u ON r.user_id = u.user_id GROUP BY r.user_id, u.username ORDER BY number_of_reviews DESC LIMIT 10;")
reviews = cursor.fetchall()
print("\nTop 10 users with most reviews:")
for review in reviews:
    print(review)

# بستن اتصال
cursor.close()
conn.close()

# DONE 