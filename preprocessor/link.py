import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from functools import reduce


def url_text_extractor(url: str) -> str:
    html = urlopen(url).read()

    soup = BeautifulSoup(html, features="html.parser")

    # kill script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


def url_text_extractor_v2(url: str) -> tuple[str, str]:
    html = urlopen(url).read()
    parse_html = BeautifulSoup(html, "lxml")
    paragraphs = parse_html.find_all("p")
    content = reduce(lambda x, y: x + y.text, paragraphs, "")
    content = re.sub(r"\[[0-9]*\]", " ", content)
    content = re.sub(r"\s+", " ", content)
    # Removing special characters and digits
    formatted_content = re.sub("[^a-zA-Z]", " ", content)
    formatted_content = re.sub(r"\s+", " ", formatted_content)

    return content, formatted_content
