"""Basic VADER sentiment scoring."""
import nltk
nltk.download("vader_lexicon")

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

score = sia.polarity_scores("I love this product, it works great!")
print(score)
# {'neg': 0.0, 'neu': 0.536, 'pos': 0.464, 'compound': 0.6249}

score = sia.polarity_scores("Terrible experience, would not recommend.")
print(score)
# {'neg': 0.577, 'neu': 0.423, 'pos': 0.0, 'compound': -0.4767}
