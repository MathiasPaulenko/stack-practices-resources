import requests

def get_service_token() -> str:
    response = requests.post('https://auth.example.com/token', data={
        'grant_type': 'client_credentials',
        'client_id': 'payment-service',
        'client_secret': get_secret('payment-service-secret'),
        'scope': 'read:orders write:orders',
    })
    token_data = response.json()
    return token_data['access_token']
