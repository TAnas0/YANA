class NewsStory:
    def __init__(self, source: str, title: str, summary: str = None, content: str = None):
        self.source = source
        self.title = title
        self.summary = summary
        self.content = content

        # self.link = 
        # self.published_at = 

    def __repr__(self):
        return f"<NewsStory source={self.source} title={self.title}>"

    def __eq__(self, other):
        if isinstance(other, NewsStory):
            return self.source == other.source and self.title == other.title
        return False

    def __hash__(self):
        # Create a hash based on multiple attributes
        return hash((self.source, self.title))

