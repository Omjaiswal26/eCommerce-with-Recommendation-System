import requests

url = "https://sandbox.cashfree.com/pg/orders"

payload = {
    "customer_details": {
        "customer_id": 'abc',
        "customer_email": 'abs@gmail.com',
        "customer_phone": '9898989898',
    },
    "order_id": '1223264',
    "order_amount": 500,
    "order_currency": "INR"
}
headers = {
    "x-api-version": "2021-05-21",
    "accept": "application/json",
    "x-client-id": "3208122e4902498c1870bcc2d2218023",
    "x-client-secret": "d22216c5f5c5b9f2371ef2ff55922ec0b15a79c1",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()

print(response.text)
