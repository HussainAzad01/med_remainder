from django.conf import settings
import requests
import random

def send_otp(phone):
    try:
        otp = random.randint(1000, 9999)
        url = f"https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone}/{otp}"
        response = requests.get(url)
        return otp
    except Exception as e:
        return None




