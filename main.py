import time
import requests
import feedparser
from models import NewsStory
from analysis.main import extract_locations, extract_names, extract_all, compare_news_stories, compare_news_stories_by_entities


def fetch_cnn_stories():
    cnn_rss_url = "http://rss.cnn.com/rss/edition.rss"
    feed = feedparser.parse(cnn_rss_url)
    
    stories = []
    for entry in feed.entries:
        title = entry.title
        # summary = entry.summary
        # content = entry.get('content', [{}])[0].get('value', '')  # If content exists, use it
        story = NewsStory("cnn", title)
        stories.append(story)
    
    return stories


def fetch_cnbc_stories():
    cnbc_rss_url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    feed = feedparser.parse(cnbc_rss_url)
    
    stories = []
    for entry in feed.entries:
        title = entry.title
        # summary = entry.summary
        # content = entry.get('content', [{}])[0].get('value', '')
        story = NewsStory("cnbc", title)
        stories.append(story)
    
    return stories


def fetch_guardian_stories():
    guardian_rss_url = "https://www.theguardian.com/world/rss"
    feed = feedparser.parse(guardian_rss_url)
    
    stories = []
    for entry in feed.entries:
        title = entry.title
        summary = entry.summary
        # content = entry.get('content', [{}])[0].get('value', '')
        story = NewsStory("guardian", title, summary)
        stories.append(story)
    
    return stories

def fetch_new_york_times_stories():
    rss_feed = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    feed = feedparser.parse(rss_feed)

    stories = []

    for entry in feed.entries:
        story = NewsStory("nytimes", entry.title, entry.summary)
        stories.append(story)

    return stories

def fetch_sky_news_stories():
    rss_feed = "https://feeds.skynews.com/feeds/rss/world.xml"
    feed = feedparser.parse(rss_feed)

    stories = []

    for entry in feed.entries:
        story = NewsStory("skynews", entry.title, entry.summary)
        stories.append(story)

    return stories

def fetch_rt_stories():
    rss_feed = "https://www.rt.com/rss/news/"
    feed = feedparser.parse(rss_feed)

    stories = []

    for entry in feed.entries:
        story = NewsStory("rt", entry.title, entry.summary)
        stories.append(story)

    return stories

def fetch_cbc_stories():
    try:
        rss_feed = "https://www.cbc.ca/webfeed/rss/rss-world"
        # Fetch the RSS feed using requests with a 10-second timeout
        response = requests.get(rss_feed, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        # Parse the content with feedparser
        feed = feedparser.parse(response.content)
        # feed = feedparser.parse(rss_feed)

        stories = []

        for entry in feed.entries:
            story = NewsStory("cbc", entry.title, entry.summary)
            stories.append(story)

        return stories
    except requests.exceptions.Timeout:
        print("The request timed out after 10 seconds")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the feed: {e}")
    
    return []


def fetch_yahoo_stories():
    rss_feed = "https://www.yahoo.com/news/rss/world/"
    feed = feedparser.parse(rss_feed)

    stories = []

    for entry in feed.entries:
        story = NewsStory("yahoo", entry.title)
        stories.append(story)

    return stories


def fetch_aljazeera_stories():
    rss_feed = "https://www.aljazeera.com/xml/rss/all.xml"
    feed = feedparser.parse(rss_feed)

    stories = []

    for entry in feed.entries:
        story = NewsStory("aljazeera", entry.title)
        stories.append(story)

    return stories


