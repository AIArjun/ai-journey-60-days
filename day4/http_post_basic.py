import requests

url = "https://httpbin.org/post"

payload = {
    "name": "Arjun",
    "learning": "APIs",
    "day": 4
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    print("Server received this data:")
    print(data["json"])
else:
      print("Request failed:", response.status_code)
