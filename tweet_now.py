import os, tweepy
from dotenv import load_dotenv
load_dotenv()
c=tweepy.Client(consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SECRET"), access_token=os.getenv("ACCESS_TOKEN"), access_token_secret=os.getenv("ACCESS_SECRET"))
text="M82 BREAKOUT: PLTR $156.97 > $151.03 Otherworldly intacto | WTI $75.96 | 10:25ET @MolinaHoldings $PLTR #M82"
try:
 r=c.create_tweet(text=text)
 print(f"✅ POSTED LIVE {r.data['id']}: {text}")
except Exception as e:
 print(f"📝 DRY_RUN LOG (402 credits): {text}")
 print(f"Motivo: {e}")
 with open("tweets_log.txt","a") as f:
  f.write(text+"\n")
