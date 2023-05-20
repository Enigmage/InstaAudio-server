import re


def preprocess_text(text):
    # Remove footers and headers based on patterns or keywords
    footer_patterns = [
        r"^\d+\s*\|",  # Remove lines starting with numbers followed by a pipe symbol
        r"page \d+\s*of \d+",  # Remove "Page X of Y" patterns
        r"www\.example\.com",  # Remove specific keywords like website URLs
    ]
    for pattern in footer_patterns:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)

    # Remove section headings
    text = re.sub(
        r"\n\s*\d+\s*[A-Za-z]+\s*\n", "", text
    )  # Remove section headings like "1 Introduction"

    # Remove table of contents
    text = re.sub(
        r"table of contents", "", text, flags=re.IGNORECASE
    )  # Remove table of contents section

    # Remove page numbers
    text = re.sub(r"\n\s*\d+\s*\n", "", text)  # Remove standalone page numbers

    # Remove references and citations
    text = re.sub(r"\[\d+\]", "", text)  # Remove square bracketed numbers

    # Remove code blocks
    text = re.sub(r"\`\`\`[\s\S]*?\`\`\`", "", text)
    text = re.sub(r"\.(\s*\.)+", ".", text)

    # Remove excess whitespace and newlines
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


# def visitor_body(text, cm, tm, fontDict, fontSize):
#     y = tm[5]
#     if y > 50 and y < 720:
#         parts.append(text)
#
#
# page.extract_text(visitor_text=visitor_body)
# text_body = "".join(parts)
# print(text_body)
