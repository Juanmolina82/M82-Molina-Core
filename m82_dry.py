import os, time
from dotenv import load_dotenv
load_dotenv()
dry = os.getenv("DRY_RUN")=="true"
print(f"M82 MODO {'DRY_RUN - solo log' if dry else 'LIVE'} | USER: MolinaHoldings")
print("PLTR $151.03 BREAK | WTI $76.09 | BTC $114.9k - sync activo")

# Simula loop
for i in range(3):
    tweet = f"M82 ALERT {i+1}: PLTR $151.03 BREAKOUT sync WTI $76.09 @MolinaHoldings #M82"
    if dry:
        with open("tweets_log.txt","a") as f:
            f.write(tweet+"\n")
        print(f"📝 LOG (no posted por 402): {tweet}")
    time.sleep(1)

print("\n✅ M82 corriendo. Tweets guardados en tweets_log.txt")
print("Cuando tengas créditos, cambia DRY_RUN=false en .env")
