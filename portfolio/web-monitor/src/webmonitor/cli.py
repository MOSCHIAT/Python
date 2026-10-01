import argparse, json, sys
from pathlib import Path
from .monitor import check_urls, read_urls, report_dict, write_json_report

def build_parser():
    parser=argparse.ArgumentParser(prog="web-monitor",description="Monitor public webpages and detect content changes.")
    parser.add_argument("urls",type=Path)
    parser.add_argument("--state",type=Path,default=Path("state/web-monitor.json"))
    parser.add_argument("--report",type=Path)
    parser.add_argument("--timeout",type=float,default=10.0)
    return parser

def main(argv=None):
    args=build_parser().parse_args(argv)
    try:
        results=check_urls(read_urls(args.urls),args.state,timeout=args.timeout)
        report=report_dict(results)
        for r in results:
            suffix=f" | {r.title}" if r.title else ""
            if r.error: suffix+=f" | {r.error}"
            print(f"[{r.status}] {r.url}{suffix}")
        print(json.dumps(report["summary"],ensure_ascii=False))
        if args.report:
            write_json_report(args.report,report); print(f"Report: {args.report}")
        return 0 if report["summary"]["ERROR"]==0 else 1
    except (OSError,ValueError) as exc:
        print(f"Error: {exc}",file=sys.stderr); return 1

if __name__=="__main__":
    raise SystemExit(main())
