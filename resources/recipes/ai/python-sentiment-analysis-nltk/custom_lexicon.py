"""Customize VADER lexicon with domain-specific words."""
import nltk
nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

# Add domain-specific words for app reviews
new_words = {
    "buggy": -2.0,
    "crash": -3.0,
    "responsive": 2.0,
    "intuitive": 2.0,
    "laggy": -1.5,
    "polished": 1.5,
}
sia.lexicon.update(new_words)

print(sia.polarity_scores("The app is buggy and crashes often"))
# Now scores more negative with custom words

print(sia.polarity_scores("The interface is polished and responsive"))
# Now scores more positive with custom words
