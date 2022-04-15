#notes https://stackoverflow.com/questions/63718559/finding-most-similar-sentences-among-all-in-python

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similarity(input_text, corpus):
  cosine_sim={}

  texts_corpus = list(corpus.values())

  #remove the index 0 from the data loaded from the csv file
  texts_corpus = [str(row[0]) for row in texts_corpus]
  
  # print(texts_corpus)

  vectorizer = TfidfVectorizer()
  X = vectorizer.fit_transform(texts_corpus)

  y = vectorizer.transform([input_text])

  # threshold = 0.4

  for x in range(0,X.shape[0]):
    # if(cosine_similarity(X[x],y)>threshold):
    # print(x, ":" ,corpus[x])
    # print("Cosine similarity:",cosine_similarity(X[x],y))
    # cosine_sim.append((corpus[x][0],corpus[x][1], cosine_similarity(X[x],y)[0][0]))
    cosine_sim[list(corpus.keys())[x]] = cosine_similarity(X[x],y)[0][0]

  return cosine_sim