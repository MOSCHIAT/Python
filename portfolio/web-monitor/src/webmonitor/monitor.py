from datetime import datetime, timezone
from pathlib import Path
from .fetcher import WebMonitorError, fetch_page
from .models import CheckResult
from .state import load_state, save_state

def read_urls(path):
    if not path.is_file(): raise ValueError(f"URL list does not exist: {path}")
    urls=[]
    for raw in path.read_text(encoding="utf-8").splitlines():
        value=raw.strip()
        if value and not value.startswith("#"): urls.append(value)
    if not urls: raise ValueError("URL list is empty")
    return list(dict.fromkeys(urls))

def check_urls(urls,state_path,timeout=10.0,fetcher=fetch_page):
    previous=load_state(state_path); current=dict(previous); results=[]
    for url in urls:
        try:
            snap=fetcher(url,timeout); old=previous.get(snap.url)
            status="NEW" if old is None else ("UNCHANGED" if old==snap.content_hash else "CHANGED")
            current[snap.url]=snap.content_hash
            results.append(CheckResult(snap.url,status,snap.title,snap.content_hash,snap.status_code))
        except (ValueError,WebMonitorError) as exc:
            results.append(CheckResult(url,"ERROR","","",error=str(exc)))
    save_state(state_path,current)
    return results

def report_dict(results):
    counts={s:0 for s in ("NEW","CHANGED","UNCHANGED","ERROR")}
    for result in results: counts[result.status]+=1
    return {"checked_at":datetime.now(timezone.utc).isoformat(),"summary":counts,"results":[r.__dict__ for r in results]}

def write_json_report(path,report):
    import json
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
