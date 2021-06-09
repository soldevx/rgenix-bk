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

model = KeyedVectors.load_word2vec_format('./word2vec/GoogleNews-vectors-negative300.bin', binary=True)

# needs nltk.download('punkt')
# also nltk.download('stopwords')
# also nltk.download('wordnet')

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

def preprocess(path, stemming_method = 'porter'):
    text = extract_text(path)
    text = cleanse_text(text)
    tokens = tokenize_and_remove_stop_words(text)
    tokens = stemming(tokens, stemming_method=stemming_method)
    tokens = lemmatization(tokens)
    return tokens

def word_untokenize(l):
    return ''.join(' ' + word for word in l)[1:]

def metrics_combine(x1, x2):
    return 2 * x1 * x2 / (x1 + x2) 

def rank(path_to_job_desc : str, path_to_cvs : str) -> List[Tuple[str, float]]:
    job_desc_tokens = preprocess(path_to_job_desc)
    cv_tokens_list = [(file_path, preprocess(file_path)) for file_path in 
                        [join(path_to_cvs, file) for file in listdir(path_to_cvs)]
                     if isfile(file_path)]
    
    print('Commence tfidf')

    data = [job_desc_tokens] + [c[1] for c in cv_tokens_list]
    data = [word_untokenize(d) for d in data]
    tfidf = TfidfVectorizer().fit_transform(data)
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
    results = [(cv_tokens_list[index][0], c) for index, c in enumerate(cosine_similarities[1:])]
    results.sort(reverse=True,key=lambda x : x[1])

    for c in results:
        print(c[0], 'has similarity', c[1])

    print('Commence word2vec')
    job_desc_tokens = [word for word in tokenize_and_remove_stop_words(cleanse_text(extract_text(path_to_job_desc))) if word in model]
    cv_tokens_list = [(file_path, tokenize_and_remove_stop_words(cleanse_text(extract_text(file_path)))) for file_path in 
                        [join(path_to_cvs, file) for file in listdir(path_to_cvs)]
                     if isfile(file_path)]

    cv_tokens_list = [(c[0], [word for word in c[1] if word in model]) for c in cv_tokens_list]

    results2 = [(c[0], model.n_similarity(job_desc_tokens, c[1])) for c in cv_tokens_list]

    results2.sort(reverse=True,key=lambda x : x[1])

    for c in results2:
        print(c[0], 'has similarity', c[1])

    print('Commence blending')

    results3 = []
    for r1 in results:
        for r2 in results2:
            if r1[0] == r2[0]:
                results3.append((r1[0], metrics_combine(r1[1], r2[1])))

    results3.sort(reverse=True,key=lambda x : x[1])

    for c in results3:
        print(c[0], 'has similarity', c[1])

    
    return []

CVS_PATH = 'basic_test/appliants/'
JOB_DESC_PATH = 'basic_test/job_desc/jobdesc.pdf'
JOB_DESC_PATH2 = 'basic_test/job_desc/jobdesc2.pdf'
print('============================= Test 1 ================================')
rank(JOB_DESC_PATH, CVS_PATH)
print('============================= Test 2 ================================')
rank(JOB_DESC_PATH2, CVS_PATH)