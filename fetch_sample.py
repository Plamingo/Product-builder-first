import urllib.request
import json

url = "https://fxjtykeuznhnyctyqalc.supabase.co/rest/v1/apartment_deals?select=*&limit=5"
headers = {
    "apikey": "sb_publishable_cPFw8hOTys96SJkuG_k0ow_DOf4vxAd",
    "Authorization": "Bearer sb_publishable_cPFw8hOTys96SJkuG_k0ow_DOf4vxAd"
}

req = urllib.request.Request(url, headers=headers)
try:
  with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print("Data sample:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
  print("Error:", e)
