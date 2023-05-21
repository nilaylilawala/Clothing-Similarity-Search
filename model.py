import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

df = pd.read_csv("item.csv")

# Loading vocabulary
vocab = []
with open("vocab", "rb") as fp:
      vocab = pickle.load(fp)

# Creating Tfidf model
model = TfidfVectorizer()
model.fit(vocab)

# Save the model
pickle.dump(model, open("vectorizer_model.pickle", "wb"))
