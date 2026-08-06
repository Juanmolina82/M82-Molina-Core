import os, requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
load_dotenv('.env_x')
auth=OAuth1(os.getenv("API_KEY"), os.getenv("API_SECRET"), os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
r=requests.get("https://api.twitter.com/2/users/me", auth=auth)
print(r.status_code, r.text[:300])
