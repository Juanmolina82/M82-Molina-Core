import feedparser, requests, time

RSS = [
 "https://www.benzinga.com/feed",
 "https://www.investing.com/rss/news_25.rss"
]
NTFY="https://ntfy.sh/M82-Molina-Alerts"

seen=set()
while True:
 for url in RSS:
  d=feedparser.parse(url)
  for e in d.entries[:20]:
   t=e.title
   if any(k in t for k in ["Bezos","AMZN sells","Hormuz","WTI","PLTR","OXY","Bitdeer","KKR"]):
    if t not in seen:
     seen.add(t)
     requests.post(NTFY, data=t.encode(), headers={"Title":f"MT RADAR {t[:80]}","Tags":"mt,auto","Priority":"high"})
     print(f"CAZADO: {t}")
 time.sleep(60)
