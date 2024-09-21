import string
import nltk
import requests

from googlesearch import search
from lxml import html
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer


# helper function to generate text corpus from html elements
def generate_corpus(all_p_elements):
    corpus = ""
    for p_element in all_p_elements:
        corpus += '\n' + ''.join(p_element.findAll(text = True))
    return corpus


# preprocessing (lemmatization, removing punctuation)
def LemTokens(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def calculate_cosine_similarity(tfidf):

    # Calculate cosine_similarity
    cosine_sim_matrix = cosine_similarity(tfidf[-1], tfidf)
    
    # get index second highest value for cosine_similarity 
    # highest value will be the user_input itself
    idx = cosine_sim_matrix.argsort()[0][-2]
    cosine_sim_flattened = cosine_sim_matrix.flatten()
    cosine_sim_flattened.sort()
    req_tfidf = cosine_sim_flattened[-2]

    return idx, req_tfidf


def get_bot_response(user_input):
    # default bot response
    bot_response = "I'm sorry, I don't think I can help you with that :("
    try:
        # use the google search api to fetch top 3 search results
        google_search_results = list(search(user_input, stop=3, pause=1))
        
        # use the requests api to fetch the top result webpage
        webpage = requests.get(google_search_results[0])
        webpage_tree = html.fromstring(webpage.content)
        webpage_soup = BeautifulSoup(webpage.content, "lxml")
        
        # extract all <p> elements from webpage soup object
        all_p_list = webpage_soup.findAll('p')
        
        # generate corpus from all <p> elements
        google_search_corpus = generate_corpus(all_p_list)

        # Tokenisation
        sentence_tokens = nltk.sent_tokenize(google_search_corpus)# converts raw text to list of sentences

        # Calculate TFIDF matrix
        sentence_tokens.append(user_input)
        tfidf_vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(sentence_tokens)

        idx, req_tfidf = calculate_cosine_similarity(tfidf)
        
        if(req_tfidf==0):
            # if value of cosine_similarity == 0, similar sentence not found 
            bot_response = "I am sorry! I don't think I can help you with that at the moment..."
        else:
            bot_response = sentence_tokens[idx]
        sentence_tokens.remove(user_input)
        return bot_response

    except:
      # return the default response if corpus is empty
      if len(google_search_corpus) == 0:
        return bot_response