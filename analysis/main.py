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

