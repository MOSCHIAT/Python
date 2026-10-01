from html.parser import HTMLParser
import hashlib, re
from urllib import error, request
from .models import PageSnapshot

class WebMonitorError(RuntimeError):
    pass

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._in_title=False
        self._skip_depth=0
        self.title_parts=[]
        self.text_parts=[]

    def handle_starttag(self, tag, attrs):
        tag=tag.lower()
        if tag=="title": self._in_title=True
        elif tag in {"script","style","noscript"}: self._skip_depth+=1

    def handle_endtag(self, tag):
        tag=tag.lower()
        if tag=="title": self._in_title=False
        elif tag in {"script","style","noscript"} and self._skip_depth:
            self._skip_depth-=1

    def handle_data(self, data):
        if self._in_title: self.title_parts.append(data)
        if self._skip_depth==0 and not self._in_title:
            text=re.sub(r"\\s+"," ",data).strip()
            if text: self.text_parts.append(text)

    @property
    def title(self): return re.sub(r"\\s+"," "," ".join(self.title_parts)).strip()

    @property
    def visible_text(self): return re.sub(r"\\s+"," "," ".join(self.text_parts)).strip()

def normalize_url(url):
    value=url.strip()
    if not value: raise ValueError("URL cannot be empty")
    if not value.startswith(("http://","https://")): raise ValueError(f"Unsupported URL: {url}")
    return value

def fetch_page(url, timeout=10.0):
    url=normalize_url(url)
    req=request.Request(url, headers={"User-Agent":"WebMonitor/1.0 (+public-page-monitor)"}, method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw=response.read()
            status_code=getattr(response,"status",200)
    except error.HTTPError as exc:
        raise WebMonitorError(f"HTTP {exc.code}") from exc
    except error.URLError as exc:
        raise WebMonitorError(f"Network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise WebMonitorError("Request timed out") from exc

    parser=PageParser()
    parser.feed(raw.decode("utf-8",errors="replace"))
    text=parser.visible_text
    digest=hashlib.sha256(text.encode("utf-8")).hexdigest()
    return PageSnapshot(url,int(status_code),parser.title,text,digest)
