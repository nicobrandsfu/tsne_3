

import pandas as pd # offers data structures and operations for manipulating numerical tables
import numpy as np # array-processing package
import nltk #Natural Language toolkit
import ssl
import json

import nltk.data
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import ne_chunk
from nltk.text import Text
import string, re
from nltk.corpus import stopwords #stopwords set out of nltk corpus


# --- TXT DATA INPUT ---

# reads txt file
with open('txt/P1_Record1.txt', 'r') as myfile:
  P1_text = myfile.read()
  #print(P1_text)

# --- PREPROCESSING DATA ---

#// text into sentences
sentence = sent_tokenize(P1_text)

P1_words = word_tokenize(P1_text)
#print(P1_words)


#// REMOVE PUNCTUATION
def remove_punctuation(sentence):
    sentence = re.sub(r'[^\w\s\n\"]','',sentence)
    return sentence
cleaned_sent = [remove_punctuation(sentence) for sentence in sentence]
partial_speech = cleaned_sent[1:15]



df_2 = pd.DataFrame(P1_words, columns = ['Words'])
df_2.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_3/json/P1_Words.json', orient='columns')


df_1 = pd.DataFrame(cleaned_sent, columns = ['Sentences'])
#print(df_1)

df_1.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_3/json/P1_Sentences.json', orient='columns')


# y = json.dumps(partial_speech)
# print(y)

#Get the file name for the new file to write
# filter = "JSON File (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.SaveFileName("P1_Sentences", filter)
#
# # If the file name exists, write a JSON string into the file.
# if filename:
#     # Writing JSON data
#     with open(filename, 'w') as f:
#         json.dump(partial_speech, f)


#// TOKENIZE SENTENCES
partial_speech_words = [word_tokenize(sentence) for sentence in partial_speech]
#print(partial_speech_words)

#// REMOVE STOP WORDS
stop_words = list(set(stopwords.words('english')))
#print('Number of stopwords:',len(stop_words))
#print(f'First 30 stop words:\n{stop_words[:30]}')

def remove_stopword(sentence):
    return[w for w in sentence if not w in stop_words]

filtered = [remove_stopword(s) for s in partial_speech_words]
word_count = len([w for words in partial_speech_words for w in words])
word_count2 = len([w for words in filtered for w in words])

#print(f'Number of Words before removing stop words:\n{word_count}')
#print(f'Number of Words after removing stop words:\n{word_count2}')
print(filtered)

#// POS TAG THE TOKENIZED SENTENCES
#// dont need it right now!!
#POS = [nltk.pos_tag(tokenized_sent) for tokenized_sent in filtered ]
#print(POS[1:10])

#// SHOW CONCORDANCE (FROM INITIAL TEXT)
#// dont need it right now
#speech_words = Text(word_tokenize(P1_text))
#speech_words.concordance('realize')
#speech_words.concordance('realized')

#// whole text to strings (tokens)
token = word_tokenize(P1_text)
#print(token)

#// tokens into enteties like peope, nouns
#// dont need it right now
#tags = nltk.pos_tag(token)
#chunk = ne_chunk(tags)
#print(chunk)

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# initialize sentences as docs
docs = sentence

# show certain sentences
#print(f'Sentence 10:\n{sentence[10]}')
#print(f'Sentence 24:\n{sentence[24]}')
#print(f'Sentence 12:\n{sentence[12]}')


#INSTANTIARE COUNTVECTOR
cv=CountVectorizer()

# IDF WITH BETTER TRAINED DATA SET????
# this steps generates word counts for the words in your docs
word_count_vector=cv.fit_transform(docs)
word_count_vector.shape
#print(word_count_vector.shape)
#// 25 DOCS (Sentence) & 290 COLUMS (unique Words)--> (25, 290)

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

#print idf values
df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"])

# sort ascending
df_idf.sort_values(by=['idf_weights'])
#print(df_idf.sort_values)

# --- COMUTE THE TFIDF SCORE FOR THE DOCUMENTS (SENTENCES) // Tfidftransformer ---

# count matrix
count_vector=cv.transform(docs)

# tf-idf scores
tf_idf_vector=tfidf_transformer.transform(count_vector)

feature_names = cv.get_feature_names()

#get tfidf vector for first document (sentence)
first_document_vector=tf_idf_vector[0]

#print the scores
df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
df.sort_values(by=["tfidf"],ascending=False)
#print(df)
#print(tf_idf_vector[24])

# WILL BE IMPORTANT FOR TRAINING DATA SET???
# --- COMUTE THE TFIDF SCORE FOR THE DOCUMENTS (SENTENCES) // Tfidfvectorizer ---
from sklearn.feature_extraction.text import TfidfVectorizer

# settings that you use for count vectorizer will go here
tfidf_vectorizer=TfidfVectorizer(use_idf=True)

# just send in all your docs here
tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(docs)
#print(tfidf_vectorizer_vectors)

# --- GET VECTORES FOR EACH DOCUMENT AND CONVERT IT INTO 1ST JSON FILE ---

# get the first vector out (for the first document)
#first_vector_tfidfvectorizer=tfidf_vectorizer_vectors
# place tf-idf values in a pandas data frame
# df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
df = pd.DataFrame(tfidf_vectorizer_vectors.T.todense(), index=tfidf_vectorizer.get_feature_names())
print(df)
#df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_values.json', orient='values')
#df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_split.json', orient='split')
#df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_index.json', orient='index')
#df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_records.json', orient='records')
df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_3/json/vector_colums.json', orient='columns')


# # get the first vector out (for the first document)
# first_vector_tfidfvectorizer=tfidf_vectorizer_vectors[10]
# # place tf-idf values in a pandas data frame
# # df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
# df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
# print(df)
# df.sort_values(by=["tfidf"],ascending=False)
# df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_10.json', orient='index')
#
#
# # --- GET VECTORES FOR EACH DOCUMENT AND CONVERT IT INTO 2ND JSON FILE ---
#
# # second vector (cluster)
# second_vector_tfidfvectorizer=tfidf_vectorizer_vectors[24]
#
# # place tf-idf values in a pandas data frame
# # df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
# df = pd.DataFrame(second_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
# df.sort_values(by=["tfidf"],ascending=False)
# df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_24.json', orient='index')
#
# # --- GET VECTORES FOR EACH DOCUMENT AND CONVERT IT INTO 3RD JSON FILE ---
#
# # second vector (cluster)
# second_vector_tfidfvectorizer=tfidf_vectorizer_vectors[12]
#
# # place tf-idf values in a pandas data frame
# # df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
# df = pd.DataFrame(second_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"])
# df.sort_values(by=["tfidf"],ascending=False)
# df.to_json(r'/Users/NicoBrand/Documents/Projekts/tsne_1/json/vector_12.json', orient='index')
