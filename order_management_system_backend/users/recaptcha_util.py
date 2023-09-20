import requests
from django.conf import settings

def verify_recaptcha(response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': response,
    }
    response = requests.post(url, data=data)
    result = response.json()

    return result.get('success', False)
