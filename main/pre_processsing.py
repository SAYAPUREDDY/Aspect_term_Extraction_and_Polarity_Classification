"""
This particular script is used to remove all the stopwords from the reviews present in the database
Pre-Processing method for the database

Steps:
1. Read the CSV file containing the reviews
2. Remove stopwords from the reviews
3. Save the cleaned reviews to a new CSV file

"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

wordnet = WordNetLemmatizer()

file_path = 'NKD_REVIEWS_WITH_REVIEWS.csv'  # Update this with your file path
data = pd.read_csv(file_path)

if 'textTranslated' not in data.columns:
    raise ValueError("The CSV file must contain a 'reviews' column.")

reviews = data['textTranslated']

corpus = []

for review in reviews:
    cleaned_review = re.sub('[^a-zA-Z]', ' ', str(review))
    cleaned_review = cleaned_review.lower()
    words = cleaned_review.split()
    words = [wordnet.lemmatize(word) for word in words if word not in set(stopwords.words('english'))]
    cleaned_review = ' '.join(words)
    corpus.append(cleaned_review)

for cleaned_review in corpus:
    print(cleaned_review)

data['cleaned_reviews'] = corpus
data.to_csv('NKD_6k_cleaned_reviews.csv', index=False)
print("Cleaned reviews saved to 'cleaned_reviews.csv'")
