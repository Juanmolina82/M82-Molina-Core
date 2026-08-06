import requests
r = requests.post("https://ntfy.sh/M82-Molina-Alerts", data=b"TEST REAL 10:53 VET - WTI 76.44 PLTR 156.97", headers={"Title":"M82 TEST"})
print(r.status_code, r.text)
