import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import ToktokTokenizer
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('popular')

# یک‌بار برای همیشه:
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = ToktokTokenizer()

def preprocess(text):
    if pd.isna(text):
        return ""
    
    # مرحله 1: lowercase
    text = text.lower()
    
    # مرحله 2: حذف علائم نگارشی و اعداد
    text = re.sub(r'[^a-z\s]', '', text)
    
    # مرحله 3: توکن‌سازی
    tokens = tokenizer.tokenize(text)
    
    # مرحله 4: حذف stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # مرحله 5: Lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # بازسازی متن
    return ' '.join(tokens)

df = pd.read_csv("Musical_instruments_reviews.csv")
df["cleaned_review"] = df["reviewText"].apply(preprocess)
df["cleaned_summary"] = df["summary"].apply(preprocess)
# print(df[["summary", "cleaned_summary"]].head(5))

# creating new  an d cleaned csv file:
df.to_csv("Dataset_cleaned.csv", index=False)
