import requests
from html.parser import HTMLParser
from minicode.tools.decorator import tool


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


@tool
def web_fetch(url: str, timeout: int = 30):
    """
    Fetch content from a URL

    url: URL to fetch
    timeout: request timeout in seconds
    """

    timeout = min(timeout, 30)

    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=timeout,
    )
    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")
    text = resp.text

    if "text/html" in content_type:
        parser = _TextExtractor()
        parser.feed(text)
        text = " ".join(parser.text)

    return text[:5000]
