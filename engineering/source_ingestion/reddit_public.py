"""Minimal public Reddit listing collector for discovery, not evidence."""
import argparse, json
from pathlib import Path
import requests

ALLOWED=("title","created_utc","score","num_comments","permalink","subreddit")
def sanitize_listing(payload):
    rows=[]
    for child in payload.get("data",{}).get("children",[]):
        data=child.get("data",{}); row={key:data.get(key) for key in ALLOWED}
        if row["permalink"]: row["url"]="https://www.reddit.com"+row.pop("permalink")
        rows.append(row)
    return rows
def collect(subreddit,query,user_agent):
    url=f"https://www.reddit.com/r/{subreddit}/search.json"
    r=requests.get(url,params={"q":query,"restrict_sr":"on","sort":"new","limit":100},headers={"User-Agent":user_agent},timeout=30);r.raise_for_status();return sanitize_listing(r.json())
def main():
    p=argparse.ArgumentParser();p.add_argument("subreddit");p.add_argument("query");p.add_argument("output",type=Path);p.add_argument("--user-agent",required=True);a=p.parse_args();rows=collect(a.subreddit,a.query,a.user_agent);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(rows,indent=2),encoding="utf-8")
if __name__=="__main__":main()
