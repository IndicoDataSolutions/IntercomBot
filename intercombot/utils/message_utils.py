from html2text import HTML2Text

HTML_CONVERTER = HTML2Text()
HTML_CONVERTER.ignore_links = False
HTML_CONVERTER.escape_all = True

def extract_messages_text(messages):
    """
    @param messages - conversation messages from intercom REST endpoint
    @return concatenated plaintext messages
    """
    texts = []
    for message in messages:
        if not message.body:
            continue
        text = HTML_CONVERTER.handle(message.body).strip()
        if text:
            texts.append(text)
    return "\n".join(texts)
