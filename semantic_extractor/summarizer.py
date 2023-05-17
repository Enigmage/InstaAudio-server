import nltk
import heapq
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

    for word in freq.keys():
        freq[word] = freq[word] // max_freq

    sent_scores = defaultdict(lambda: 0)
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            # if len(sent.split(" ")) < 30:
            sent_scores[sent] += freq[word]

    summary = heapq.nlargest(15, sent_scores)

    return " ".join(summary)
