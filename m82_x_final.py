import tweepy, os
from dotenv import load_dotenv
load_dotenv('.env_x')
c=tweepy.Client(
 consumer_key=os.getenv("API_KEY"),
 consumer_secret=os.getenv("API_SECRET"),
 access_token=os.getenv("ACCESS_TOKEN"),
 access_token_secret=os.getenv("ACCESS_SECRET")
)
msg="M82 REALTIME LIVE: PLTR $151.03 BREAK + WTI $76.09 < $76.50 Bessent sync. Hunter V5 + X @MolinaHoldings ONLINE #M82 #PLTR #Oil"
try:
 r=c.create_tweet(text=msg)
 print(f"✅ POSTED {r.data['id']}\n{msg}")
except Exception as e:
 print(f"❌ {e}")
