import urllib.request
import json

url = "http://localhost:8080/news"
data = json.dumps({"text": "Внимание! Внимание! Говорит Германия!"}).encode("utf-8")

req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as response:
        print("Ответ сервера:", response.read().decode())
except Exception as e:
    print("Ошибка при отправке:", e)
