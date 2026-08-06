import requests,re,json,os,html,time
from datetime import datetime
NTFY="https://ntfy.sh/M82-Molina-Alerts"
KEYWORDS=["bessent","hormuz","strait","qatar","oman","iran","palantir","deutsche bank","caterpillar","amd","pfizer"]
BLACKLIST=["al jazeera &#8211;","world news and video"]
SEEN_FILE="m82_news_seen.json"
seen=json.load(open(SEEN_FILE)) if os.path.exists(SEEN_FILE) else []
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0"})
print("--- M82 NEWS HUNTER V4 FIX ---")
while True:
 try:
  r=s.get("https://finance.yahoo.com/rss/headline?s=CL=F,BZ=F,PLTR,CAT,AMD,PFE,BP,XOM",timeout=8).text
  items=re.findall(r'<item>.*?<title>(.*?)</title>',r,flags=re.DOTALL)
  for raw in items[:12]:
   tc=html.unescape(raw).strip()
   if len(tc)<15: continue
   if any(b in tc.lower() for b in BLACKLIST): continue
   if any(kw in tc.lower() for kw in KEYWORDS):
    if tc not in seen:
     seen.append(tc);
     if len(seen)>400: seen.pop(0)
     open(SEEN_FILE,'w').write(json.dumps(seen))
     # Body con emoji OK, Title ASCII only
     body=f"{tc}\nSource: yahoo\n{datetime.now().strftime('%H:%M:%S VET')}"
     try:
      s.post(NTFY,data=body.encode('utf-8'),headers={"Title":f"NEWS {tc[:90]}","Priority":"high"},timeout=8)
     except Exception as e:
      print(f"NTFY ERR {e}")
     print(f"[{datetime.now().strftime('%H:%M:%S')}] NEWS {tc}")
 except Exception as e:
  print(f"NEWS ERR {e}")
 time.sleep(35)
