from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timezone, date
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

def send_otp_via_email(email):
    try:
        otp = random.randint(1000, 9999)
        subject = "Account Verification Email"
        message = f"Your verification code is {otp}"
        email_from = settings.EMAIL_HOST
        send_mail(subject, message, email_from, [email])
        return otp

    except Exception as e:
        return None

def str_to_date(reminder_date):
    if reminder_date == '':
        return None
    date_string = reminder_date
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_string, date_format).date()
    return date_object


def str_to_datetime(reminder_datetime):
    if reminder_datetime == '':
        return None
    date_string = reminder_datetime
    date_format = '%Y-%m-%dT%H:%M'
    date_object = datetime.strptime(date_string, date_format)
    return date_object




