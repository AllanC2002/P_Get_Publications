import requests

PUBLICATIONS_URL = "http://3.219.144.22:8080/my-publications"

login_data = {
    "User_mail": "allan",
    "password": "1234"
}
login_response = requests.post("http://52.203.72.116:8080/login", json=login_data)

if login_response.status_code != 200:
    print("Login failed:", login_response.status_code, login_response.text)
    exit()

token = login_response.json().get("token")
print("Token:", token)

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(PUBLICATIONS_URL, headers=headers)

print("Status:", response.status_code)

try:
    publicaciones = response.json()
    print("Publications:")
    for pub in publicaciones:
        print(f"- Text: {pub.get('Text')}")
        print(f"  Date: {pub.get('Datepublish')}")
        print(f"  Multimedia (base64): {pub.get('Multimedia')[:30]}...")  # Part of base 64
        print(f"  Status: {pub.get('Status')}")
        print(f"  Likes: {pub.get('Likes')}")
        print()
except Exception as e:
    print("Erroe:", str(e))
    print("Response:", response.text)
