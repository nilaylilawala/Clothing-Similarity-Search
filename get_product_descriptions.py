import ast
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pickle


productcontent = []
productlinks = []
baseurl = "https://www.flipkart.com"

# Load productlinks
with open("productlinks", "rb") as fp:
      productlinks = pickle.load(fp)

# Scraping each product and extract the meta data
for link in productlinks:
        r = requests.get(baseurl+link)
        soup = BeautifulSoup(r.text, 'html.parser')
        s = soup.find(id="jsonLD").text
        try:
            title_name = soup.find("span", {"class": "B_NuCI"}).text
        except:
            title_name = None
        data = ast.literal_eval(s)
        if(len(data)>=1):
                data = data[0]

                try:
                        brand = data["brand"]["name"]
                except:
                        brand = None
                try:
                        title = title_name
                except:
                        title = None
                try:
                        name = data["name"]
                except:
                        name = None
                try:
                        price = data["offers"]["price"]
                except:
                        price = None
                try:
                        rating = data["aggregateRating"]["ratingValue"]
                except:
                        rating = None
                
                new_product = {
                        "Brand": brand,
                        "Title": title,
                        "Name": name,
                        "Price": price,
                        "Rating": rating,
                        "URL": (baseurl+link) 
                }
                productcontent.append(new_product)

replacements = {
    "t-shirt": "tshirt",
    "t-shirts": "tshirt",
    "tee": "tshirt",
    "man": "men",
    "woman": "women",
    "(" : "",
    ")" : "",
    "  ": " "
}

stemmer = PorterStemmer()

# Lemmatiation
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text))

# Text preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    #Replace specific words
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

    #Normalize tokens
    tokens = [lemmatize_stemming(token) for token in tokens]
        
    # Return the preprocessed tokens as a list
    return ' '.join(tokens)


# Creating a DataFrame of items
df = pd.DataFrame(productcontent)

# Drop NULL Rows
df = df.dropna()

# Merging 2 columns "Name" and "Title" as "Description"
df["Description"] = df["Name"] + " " + df["Title"]

# Preprocess raw text
df["Clean_Text"] = df["Description"].apply(lambda x: preprocess_text(x))

# Building Vocabulary
vocab = set()

for sentence in df["Clean_Text"]:
    for word in sentence.split():
        vocab.add(word)

# Save the Product Description Dataframe
df.to_csv("Item.csv")

# Save the vocabulary for further use
vocab = list(vocab)
with open("vocab", "wb") as fp:
    pickle.dump(vocab, fp)

