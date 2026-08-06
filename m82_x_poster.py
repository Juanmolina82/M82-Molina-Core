import tweepy, os
from dotenv import load_dotenv
load_dotenv('.env_x')
client=tweepy.Client(
 consumer_key=os.getenv("API_KEY"),
 consumer_secret=os.getenv("API_SECRET"),
 access_token=os.getenv("ACCESS_TOKEN"),
 access_token_secret=os.getenv("ACCESS_SECRET")
)
msg="M82 REALTIME: PLTR $151.03 BREAK > $151 Otherworldly intacto + WTI $76.09 < $76.50 Bessent deal sync. Engine ONLINE @MolinaHoldings #PLTR #Oil #M82"
try:
 r=client.create_tweet(text=msg)
 print(f"✅ TWEET OK ID {r.data['id']}")
except Exception as e:
 print(f"❌ FAIL: {e}")
