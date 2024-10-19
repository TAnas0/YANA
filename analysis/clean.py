import contractions
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup


def lowercase_text(text: str):
    return text.lower()


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_extra_whitespace(text):
    return ' '.join(text.split())


def remove_html(text):
    if text:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    else:
        return None


def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)


def remove_advertisment_tags(text: str) -> str:
    """
    Removes advertisement or repetitive text in a NewsStory, such as "Read Full Article at RT.com"
    """
    return text.replace("Read Full Article at RT.com", "")


# Download stopwords
nltk.download('stopwords')

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word not in stop_words])


# Download WordNet
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def lemmatize_text(text):
    # TODO improve lemmatization, e.g. iranian = iran
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])


def expand_contractions(text):
    return contractions.fix(text)


import spacy

# Load spaCy's NER model
nlp = spacy.load("en_core_web_sm")

# Function to replace location entities using spaCy NER
def map_location_entities_with_ner(text, location_map):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # "GPE" stands for geopolitical entities
            for canonical, variants in location_map.items():
                if ent.text in variants:
                    text = text.replace(ent.text, canonical)
    return text

def preprocess_text(text):
    if text in [None, ""]:
        return ""
    text = remove_advertisment_tags(text)
    text = lowercase_text(text)
    text = remove_html(text)
    text = remove_punctuation(text)
    # text = remove_special_characters(text)
    text = remove_extra_whitespace(text)
    text = expand_contractions(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    
    return text
