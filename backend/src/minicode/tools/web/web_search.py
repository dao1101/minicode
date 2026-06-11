import requests
from html.parser import HTMLParser
from minicode.tools.decorator import tool


class _DDGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._in_result = False
        self._link = ""
        self._title = ""
        self._tag = ""

    def handle_starttag(self, tag, attrs):
        self._tag = tag
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            href = attrs["href"]
            self._link = href if href is not None else ""
            if self._link.startswith("//duckduckgo.com/l/"):
                self._in_result = True
                self._title = ""

    def handle_data(self, data):
        if self._in_result and self._tag == "a":
            self._title += data

    def handle_endtag(self, tag):
        if self._in_result and tag == "a":
            self._in_result = False
            if self._title.strip():
                self.results.append(
                    {
                        "title": self._title.strip(),
                        "url": self._link,
                    }
                )


@tool
def web_search(query: str, max_results: int = 5):
    """
    Search the web for information

    query: search query
    max_results: max number of results
    """

    resp = requests.get(
        "https://lite.duckduckgo.com/lite/",
        params={"q": query},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )
    resp.raise_for_status()

    parser = _DDGParser()
    parser.feed(resp.text)

    return parser.results[:max_results]
