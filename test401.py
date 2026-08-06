import tweepy, os
from dotenv import load_dotenv
load_dotenv('.env_x')
c=tweepy.Client(consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SECRET"), access_token=os.getenv("ACCESS_TOKEN"), access_token_secret=os.getenv("ACCESS_SECRET"))
try:
 r=c.create_tweet(text="M82 LIVE REALTIME: PLTR $151.03 BREAK + WTI $76.09 + BTC $114,900 sync @MolinaHoldings #M82 #PLTR")
 print(f"✅ POSTED {r.data['id']}")
except Exception as e:
 print(f"❌ {e}")
