import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from functools import reduce

spoof_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}


def url_text_extractor(url: str) -> tuple[str, str]:
    req = Request(url, headers=spoof_headers)
    html = urlopen(req).read()

    soup = BeautifulSoup(html, features="html.parser")

    # kill script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)
    text = re.sub(r"\[[0-9]*\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    formatted_text = re.sub("[^a-zA-Z]", " ", text)
    formatted_text = re.sub(r"\s+", " ", formatted_text)

    return text, formatted_text


def url_text_extractor_v2(url: str) -> tuple[str, str]:
    req = Request(url, headers=spoof_headers)
    html = urlopen(req).read()
    parse_html = BeautifulSoup(html, "lxml")
    paragraphs = parse_html.find_all("p")
    content = reduce(lambda x, y: x + y.text, paragraphs, "")
    content = re.sub(r"\[[0-9]*\]", " ", content)
    content = re.sub(r"\s+", " ", content)
    # Removing special characters and digits
    formatted_content = re.sub("[^a-zA-Z]", " ", content)
    formatted_content = re.sub(r"\s+", " ", formatted_content)

    return content, formatted_content
