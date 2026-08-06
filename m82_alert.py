import requests
def send_alert(msg):
    r = requests.post("https://ntfy.sh/M82-Molina-Alerts", data=msg.encode(), headers={"Title":"M82","Priority":"high","Tags":"rocket"})
    print(f"{'✅' if r.status_code==200 else '⚠️'} {r.status_code}")
send_alert("SNDK TEST — Pipeline V6.6 LIVE")
