import nltk
import heapq
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def abstractive_summarizer(text: str) -> str:
    tokenizer = AutoTokenizer.from_pretrained("T5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("T5-base", return_dict=True)
    inputs = tokenizer.encode(
        "sumarize: " + text, return_tensors="pt", max_length=512, truncation=True
    )
    output = model.generate(inputs, min_length=100, max_length=150)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary.strip()


def extractive_summarizer(text: str, formatted_text: str) -> str:
    sentences = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words("english")

    freq = defaultdict(lambda: 0)
    max_freq = -1
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            w = word.lower()
            freq[w] += 1
            max_freq = max(max_freq, freq[w])

    for word in freq.keys():
        freq[word] = freq[word] // max_freq

    sent_scores = defaultdict(lambda: 0)
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if len(sent.split(" ")) < 30:
                sent_scores[sent] += freq[word]

    summary = heapq.nlargest(15, sent_scores)

    return " ".join(summary)
