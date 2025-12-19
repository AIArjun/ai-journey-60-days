import requests
response = requests.get("http://127.0.0.1:8000/hello")
data = response.json()
print("Response from server:", data)
