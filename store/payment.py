import requests
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def create_payment_session(request, order):
    try:
        # Step 1: Create payment intention
        intention_data = create_payment_intention(request, order)  # Pass request here
        client_secret = intention_data.get('client_secret')
        
        if not client_secret:
            raise Exception("Failed to get client secret")
        
        # Step 2: Generate unified checkout URL
        checkout_url = f"https://accept.paymob.com/unifiedcheckout/?publicKey={settings.PAYMOB_PUBLIC_KEY}&clientSecret={client_secret}"
        logger.info(f"Payment URL generated: {checkout_url}")
        return {'payment_url': checkout_url}
    
    except Exception as e:
        logger.error(f"Payment session creation failed: {str(e)}")
        raise

def create_payment_intention(request, order):  # Added request parameter
    try:
        url = "https://accept.paymob.com/api/acceptance/payment_intents"
        payload = {
            "api_key": settings.PAYMOB_API_KEY,
            "amount_cents": int(order.get_total_cost() * 100),
            "currency": "EGP",
            "payment_methods": ["card", "wallet"],
            "billing_data": {
                "apartment": "NA", 
                "email": order.email,
                "floor": "NA",
                "first_name": order.first_name,
                "street": order.address,
                "building": "NA",
                "phone_number": "+201234567890",
                "shipping_method": "NA",
                "postal_code": order.postal_code,
                "city": order.city,
                "country": "EG",
                "last_name": order.last_name,
                "state": "NA"
            },
            "customer": {
                "first_name": order.first_name,
                "last_name": order.last_name,
                "email": order.email,
            },
            "items": [{
                "name": f"Order #{order.id}",
                "amount_cents": int(order.get_total_cost() * 100),
                "description": f"Order #{order.id}",
                "quantity": 1
            }],
            "success_url": request.build_absolute_uri(reverse('store:payment_success', args=[order.id])),
            "failure_url": request.build_absolute_uri(reverse('store:payment_cancel', args=[order.id])),
        }
        
        logger.info(f"Creating payment intention with payload: {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Payment intention creation failed: {str(e)}")
        raise
