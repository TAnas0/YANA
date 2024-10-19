# Analysis of news
import numpy as np
import spacy
from models import NewsStory
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools
from analysis.clean import remove_html
from analysis.utils import remove_elements
from sklearn.cluster import DBSCAN
from nltk.corpus import wordnet


# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")


#################################
## Named Entities
#################################
def extract_locations(news_story: NewsStory):
    """Extracts the identified locations from title, summary, or content"""
    # Combine text fields for analysis
    text = " ".join(filter(None, [news_story.title, news_story.summary, news_story.content]))
        
    # Apply spaCy NLP pipeline
    doc = nlp(text)
    
    # Find location entities (GPE = Geopolitical Entity)
    gpes = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"] and ent.text.lower() not in gpes:  # GPE indicates countries, cities, states
            gpes.append(ent.text.lower())

    return gpes


def extract_names(news_story: NewsStory):
    """Extracts names of people from the given text"""
    text = " ".join(filter(None, [news_story.title, news_story.summary, news_story.content]))
    doc = nlp(text)
    names = [ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"]
    return names


def extract_all_named_entities(news_story: NewsStory):
    """
    Extracts named entities from a news story using natural language processing (NLP).

    This function processes the combined text of the news story's title, summary, and content
    to extract various types of named entities, including:
    
    - **names**: People mentioned in the text (labeled as `PERSON`).
    - **locations**: Geographic locations, including countries, cities, and other geographical entities 
      (labeled as `GPE` or `LOC`).
    - **orgs**: Organizations mentioned in the text (labeled as `ORG`).
    - **events**: Named events, such as conferences, wars, or major incidents (labeled as `EVENT`).
    - **products**: Products mentioned, such as devices or services (labeled as `PRODUCT`).
    
    Args:
        news_story (NewsStory): An object containing the title, summary, and content of a news story.

    Returns:
        dict: A dictionary containing lists of extracted named entities, categorized by type:
    """
    text = " ".join(filter(None, [news_story.title, news_story.summary, news_story.content]))
    doc = nlp(text)
    names = [ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"]
    locations = [ent.text.lower() for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    orgs = [ent.text.lower() for ent in doc.ents if ent.label_ == "ORG"]
    events = [ent.text.lower() for ent in doc.ents if ent.label_ == "EVENT"]
    products = [ent.text.lower() for ent in doc.ents if ent.label_ == "PRODUCT"]
    return {
        "names": names,
        "locations": locations,
        "orgs": orgs,
        "events": events,
        "products": products,
        # "datetimes": datetimes,
    }


#################################
## Semantic Analysis
#################################

def get_canonical_synonym(word):
    synsets = wordnet.synsets(word)
    if word.lower() == "russia": # Converted wrongly to Soviet_Union
        return word
    if synsets:
        # Get the first lemma (canonical form) of the first synset (sense of the word)
        return synsets[0].lemmas()[0].name().replace("_", " ")
    return word

def text_turn_to_canonical_roots(text):
    # For all entities in a text, turn them to the root canonical synonym
    doc = nlp(text)

    for entity in doc.ents:
        text = text.replace(entity.text, get_canonical_synonym(entity.text)) # TODO fix. should only replace full words, not all occurences (for example "US")
    return text

##################################
## Comparing NewsStories
##################################

def cluster_news_stories(news_stories: [NewsStory], strategy: str = "count"):
    """
    Groups news articles dealing with the same event, people, etc.
    """
    if strategy == "count":
        vectorizer = CountVectorizer()
    if strategy == "tf_idf":
        vectorizer = TfidfVectorizer(stop_words='english')
    else:
        raise ValueError(f"Specified strategy not supported: {strategy}")

    story_preprocessed_text = [story.preprocess_text() for story in news_stories]
    matrix = vectorizer.fit_transform(story_preprocessed_text)
    similarity_matrix = cosine_similarity(matrix, matrix)

    # Apply DBSCAN on the similarity matrix (treat similarity as a distance)
    cluster_labels = cluster_with_dbscan(similarity_matrix, eps=0.8, min_samples=2)

    # The 'cluster_labels' will have the assigned cluster or -1 for noise/outliers
    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []  # Initialize an empty list for this cluster
        clusters[label].append(news_stories[i])  # Add the news story to the correct cluster

    return clusters


def cluster_with_dbscan(similarity_matrix, eps, min_samples):
    distance_matrix = np.maximum(1 - similarity_matrix, 0)
    dbscan = DBSCAN(eps, min_samples, metric='precomputed')
    cluster_labels = dbscan.fit_predict(distance_matrix)
    return cluster_labels


def name_group_of_news_stories(news_stories, top: int = 5):
    """
    Generate a name for a group of news stories based on the top N  keywords with the highest TF-IDF scores

    Args:
        news_stories (list): A list of news story objects, each containing text to be processed
        top (int): The number of top keywords to return

    Returns:
        str: A string of the top N keywords, separated by commas, representing the main topics 
        of the combined news stories
    """
    combined_text = ' '.join([news_story.preprocess_text() for news_story in news_stories])

    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    # ! TF-IDF on a list of a single text? give multiple texts, or just use Count after removing stopwords
    matrix = vectorizer.fit_transform([combined_text])
    feature_names = vectorizer.get_feature_names_out()
    
    # Get the TF-IDF scores for the words
    tfidf_scores = matrix.toarray().flatten()
    
    # Get the top N words based on their TF-IDF score
    top_indices = tfidf_scores.argsort()[-top:][::-1]
    top_keywords = [feature_names[index] for index in top_indices]
    
    return ", ".join(top_keywords)


print()