import requests
response = requests.post('http://localhost:8000/heroes/1')
print(response.json())