# -*- coding: utf-8 -*-
from typing import List, Tuple
from re import sub
from pdfminer.high_level import extract_text

from os import listdir
from os.path import isfile, join

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer

from gensim.models import KeyedVectors

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

model = KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

def cleanse_text(text : str) -> str:
    # remove numbers and special characters
    clean_text = sub('[^a-zA-Z\-\'\s]', '', text)
    # transform all whitespaces into a single space
    clean_text = sub('\s+', ' ', clean_text)
    # a few common transformations
    clean_text = sub('\'ll', ' will', clean_text)
    clean_text = sub('n\'t', ' not', clean_text)
    clean_text = sub('\'d', ' would', clean_text)
    clean_text = sub('\'ve', ' have', clean_text)
    clean_text = sub('\'m', ' am', clean_text)
    clean_text = sub('\'re', ' are', clean_text)
    clean_text = sub('what\'s', 'what is', clean_text)
    # remove single letter words and lowercase everything
    clean_text = sub('^[^\s] | [^\s]$ | [^\s] ', ' ', clean_text)
    return clean_text

def tokenize_and_remove_stop_words(text : str) -> List[str]:
    tokens = word_tokenize(text)
    return [word for word in tokens if not word in stopwords.words()]

def stemming(tokens : List[str], stemming_method : str = 'porter') -> List[str]:
    stemmer = None

    if stemming_method == 'porter':
        stemmer = PorterStemmer()
    elif stemming_method == 'snowball':
        stemmer = SnowballStemmer()
    else:
        stemmer = LancasterStemmer()

    return [stemmer.stem(word) for word in tokens]

def lemmatization(tokens : List[str], lemming_method : str = '') -> List[str]:
    lemmer = WordNetLemmatizer()
    return [lemmer.lemmatize(word) for word in tokens]

def word_untokenize(l):
    return ''.join(' ' + word for word in l)[1:]

def preprocess(fileIn, stemming_method = 'porter'):
    # initial preprocessing
    text = extract_text(fileIn)
    text = cleanse_text(text)
    tokens = tokenize_and_remove_stop_words(text)

    # create word2vec tokens
    word2vec_tokens = [word for word in tokens if word in model]

    # continue preprocessing for tfidf tokens
    tokens = stemming(tokens, stemming_method=stemming_method)
    tokens = lemmatization(tokens)
    tokens = word_untokenize(tokens)

    return tokens, word2vec_tokens

def combine_metrics(x1, x2):
    return 2 * x1 * x2 / (x1 + x2) 

def rank(jobdesc_preprocess, cvs_preprocess):
    jobdesc_preprocess_tfidf, jobdesc_preprocess_word2vec = jobdesc_preprocess
    cvs_preprocess_tfidf, cvs_preprocess_word2vec = cvs_preprocess
    # tfidf
    tfidf = TfidfVectorizer().fit_transform([jobdesc_preprocess_tfidf] + cvs_preprocess_tfidf)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    scores_tfidf = cosine_similarities[1:]
    #word2vec
    scores_word2vec = [model.n_similarity(jobdesc_preprocess_word2vec, prep) for prep in cvs_preprocess_word2vec]
    # final scores
    scores_final = [combine_metrics(s1, s2) for s1, s2 in zip(scores_tfidf, scores_word2vec)]
    return scores_final

