import nltk
from collections import defaultdict


def nlp_summarizer(text: str, formatted_text: str) -> str:
    sentences = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words("english")

    freq = defaultdict(lambda: 0)
    max_freq = -1
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            freq[word] += 1
            max_freq = max(max_freq, freq[word])

    return ""
