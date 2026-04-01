import requests

url = "https://api.deepai.org/api/nsfw-detector"
headers = {"api-key": "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"}
response = requests.post(
    url,
    files={
        "image": open("1.jpg", "rb"),
    },
    headers=headers,
)
print(response.text)
