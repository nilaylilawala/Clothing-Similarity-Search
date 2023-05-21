import pickle
import pandas as pd
import sys
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Load Tfidf model
model = pickle.load(open("vectorizer_model.pickle", "rb"))

# Read item csv
df = pd.read_csv("item.csv")

# Some necessary replacements in text
replacements = {
    "t-shirt": "tshirt",
    "t-shirts": "tshirt",
    "tee": "tshirt",
    "man": "men",
    "woman": "women",
    "(": "",
    ")": "",
    "  ": " "
}

stemmer = PorterStemmer()


# Lemmatization
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text))


# Preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Replace specific words
    for i, j in replacements.items():
        text = text.replace(i, j)

    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    tokens = list(set(tokens))

    # Remove special characters and numbers
    tokens = [token for token in tokens if token.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Normalize tokens
    tokens = [lemmatize_stemming(token) for token in tokens]

    # Return the preprocessed tokens as a list
    return ' '.join(tokens)


# Computing cosine similarity between 2 vectors
def compute_similarity(desc1, desc2, model):
    # Preprocess the item descriptions
    preprocessed_desc1 = preprocess_text(desc1)
    preprocessed_desc2 = desc2

    # Initialize the vectors
    vector1 = model.transform([preprocessed_desc1])
    vector2 = model.transform([preprocessed_desc2])

    vector1 /= len(preprocessed_desc1)
    vector2 /= len(preprocessed_desc2)

    # Compute the cosine similarity between the two vectors
    similarity_score = cosine_similarity(vector1, vector2)[0][0]

    return similarity_score


# Find the top N similar items from two given descriptions
def find_similar_items(desc1, database, model, top_n):
    # Sort the database items by similarity to the descriptions
    database['Similarity'] = database['Clean_Text'].apply(lambda x: compute_similarity(desc1, x, model))
    sorted_items = database.sort_values(by=['Similarity', 'Rating'], ascending=False)

    # Get the top N similar items
    top_similar_items = sorted_items.head(top_n)[["Name", "URL", "Similarity", ]]

    return top_similar_items


# description1 = "sneakers for women"
top_n = 10
description1 = sys.argv[1]
similar_items = find_similar_items(description1, df, model, top_n)

print(similar_items)
