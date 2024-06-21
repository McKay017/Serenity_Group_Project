# payments/utils.py

import requests
from requests.auth import HTTPBasicAuth
from .mpesa_credentials import (
    CONSUMER_KEY, CONSUMER_SECRET, 
    MPESA_ENV, LIPANAMPESA_ONLINE_SHORTCODE, LIPANAMPESA_ONLINE_PASSKEY
)
import base64
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_mpesa_token():
    try:
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" if MPESA_ENV == 'sandbox' else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        
        response = requests.get(auth_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
        response.raise_for_status()
        mpesa_token = response.json()['access_token']
        return mpesa_token
    except Exception as e:
        logger.error(f'Error obtaining M-Pesa token: {e}')
        raise

def lipa_na_mpesa_online(phone_number, amount, account_reference, transaction_desc, callback_url):
    try:
        access_token = get_mpesa_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" if MPESA_ENV == 'sandbox' else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((LIPANAMPESA_ONLINE_SHORTCODE + LIPANAMPESA_ONLINE_PASSKEY + timestamp).encode('utf-8')).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        payload = {
            "BusinessShortCode": LIPANAMPESA_ONLINE_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": float(amount),  # Convert Decimal to float
            "PartyA": phone_number,
            "PartyB": LIPANAMPESA_ONLINE_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        logger.debug(f'API URL: {api_url}')
        logger.debug(f'Request Headers: {headers}')
        logger.debug(f'Request Payload: {payload}')

        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Error in lipa_na_mpesa_online: {e}, Response: {e.response.json() if e.response else "No response"}')
        raise
