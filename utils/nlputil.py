import nltk
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

def cleanText():
    en_stop_words = stopwords.words('english')
    wordnet_lemmatizer = WordNetLemmatizer()
    exclusion_list = '|'.join(['[^a-zA-Z]','rt', 'http', 'co', 'RT'])
    def clean(text: str) -> str:
        words = re.sub(exclusion_list,  ' ', text).lower().split()
        words = [word for word in words if word not in en_stop_words]
        words = [wordnet_lemmatizer.lemmatize(word) for word in words]
        # list comprehension performs better in most cases than built-in func
        # clean_words= filter(lambda word: word not in en_stop_words, words)
        # clean_words = map(lambda word: wordnet_lemmatizer.lemmatize(word), clean_words)
        return ' '.join(words)
    return clean

def sentiment(text: str) -> int:
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 1
    elif polarity == 0:
        return 0
    else:
        return -1
        
