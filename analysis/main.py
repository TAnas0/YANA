# Analysis of news
import numpy as np
import spacy
from models import NewsStory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def extract_all(news_story: NewsStory):
    """Extracts names of people from the given text."""
    text = " ".join(filter(None, [news_story.title, news_story.summary, news_story.content]))
    doc = nlp(text)
    names = [ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"]
    locations = [ent.text.lower() for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    orgs = [ent.text.lower() for ent in doc.ents if ent.label_ == "ORG"]
    events = [ent.text.lower() for ent in doc.ents if ent.label_ == "EVENT"]
    products = [ent.text.lower() for ent in doc.ents if ent.label_ == "PRODUCT"]
    # datetimes = [ent.text.lower() for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]
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

