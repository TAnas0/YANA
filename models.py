from analysis.clean import (
    lowercase_text,
    remove_extra_whitespace,
    remove_html,
    remove_punctuation,
    remove_special_characters,
    remove_stopwords,
    lemmatize_text,
    preprocess_text,
)

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

    def preprocess_text(self) -> str:
        """
        Preprocesses the text of the NewsStory instance by applying various cleaning and normalization steps
        in preparation for AI/ML analysis
        Relevant NewsStory fields are: title, summary, content.

        Returns:
            str: The cleaned and processed text, suitable for further analysis or comparison tasks.
        """
        title = "" if self.title is None else self.title
        summary = "" if self.summary is None else self.summary
        content = "" if self.content is None else self.content

        return f"{preprocess_text(title)} {preprocess_text(summary)} {preprocess_text(content)}"

