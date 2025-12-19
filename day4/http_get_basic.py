import requests

url = "https://api.agify.io/?name=padmaja"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Success:", data)
    print("The predicted age is:", data["age"])
else:
    print("Request failed with status:", response.status_code)




