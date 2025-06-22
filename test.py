import requests

PUBLICATIONS_URL = "http://localhost:8081/my-publications"

login_data = {
    "User_mail": "ascorread1",
    "password": "1234"
}
login_response = requests.post("http://localhost:8080/login", json=login_data)

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
    print("Publicaciones del usuario:")
    for pub in publicaciones:
        print(f"- Texto: {pub.get('Text')}")
        print(f"  Fecha: {pub.get('Datepublish')}")
        print(f"  Multimedia (base64): {pub.get('Multimedia')[:30]}...")  # Part of base 64
        print(f"  Estado: {pub.get('Status')}")
        print(f"  Likes: {pub.get('Likes')}")
        print()
except Exception as e:
    print("Error al decodificar respuesta JSON:", str(e))
    print("Respuesta cruda:", response.text)
