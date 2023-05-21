# Clothing-Similarity-Search
This project is to create a machine learning model capable of receiving text describing a clothing item and returning a ranked list of links to similar items from different websites.

A function that accepts a text string, extracts its features, computes similarities with the items in the database, ranks them based on similarity, and returns the URLs of the top-N most similar items.


## Webapp
### Try here : https://asia-south1-tensile-ship-387403.cloudfunctions.net/function-2

### Write your query in this URL as https://asia-south1-tensile-ship-387403.cloudfunctions.net/function-2/?search=query
#### Ex. if you want to search for Men Black Shirts then write url as - https://asia-south1-tensile-ship-387403.cloudfunctions.net/function-2/?search=men black shirt
### Output
  ![image](https://github.com/nilaylilawala/Clothing-Similarity-Search/assets/91961900/f24124ac-1a1b-4078-8789-7e20b63b1c19)



## Requirements
pandas

numpy

scikit-learn

requests

nltk

BeautifulSoup4
