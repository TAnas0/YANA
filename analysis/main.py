# Analysis of news
import numpy as np
import spacy
from models import NewsStory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

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


def compare_news_stories(news_stories: [NewsStory]):
    """Groups news articles dealing with the same event, people, etc.

    BETTER SUITED FOR FURTHER READINGS

    # TODO Maybe generate a matrix of similarity?
    """
    texts = [" ".join(filter(None, [news_story.title, news_story.summary, news_story.content])) for news_story in news_stories]

    # Step 1: Calculate Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    grouped_articles = {}
    threshold = 0.4
    for i in range(len(news_stories)):
        # Find articles similar to the current article
        similar_indices = [j for j in range(len(news_stories)) if similarity_matrix[i][j] > threshold and i != j]

        # If similar articles are found, create a group
        if similar_indices:
            # Create a unique key for the current article
            # key = f"Article {i}: {news_stories[i].title}"
            grouped_articles[str(news_stories[i])] = [news_stories[j] for j in similar_indices]
    
    return grouped_articles


def compare_news_stories_by_entities(news_stories: [NewsStory]):
    """Groups news articles dealing with the same event, people, etc.

    BETTER SUITED FOR FURTHER READINGS

    # TODO Maybe generate a matrix of similarity?
    """
    # texts = [" ".join([news_story.title, news_story.summary, news_story.content]) for news_story in news_stories]
    story_entities = [extract_all(news_story) for news_story in news_stories]
    story_entities_text = [' '.join(' '.join(value) for value in entities.values() if value) for entities in story_entities]
    # Step 1: Calculate Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(story_entities_text)
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    grouped_articles = {}
    threshold = 0.4
    for i in range(len(news_stories)):
        # Find articles similar to the current article
        similar_indices = [j for j in range(len(news_stories)) if similarity_matrix[i][j] > threshold and i != j]

        # If similar articles are found, create a group
        if similar_indices:
            # Create a unique key for the current article
            # key = f"Article {i}: {news_stories[i].title}"
            grouped_articles[str(news_stories[i])] = [news_stories[j] for j in similar_indices]
    
    return grouped_articles
