import requests
from django.conf import settings

class PaymobAPI:
    def __init__(self):
        self.api_key = settings.PAYMOB_API_KEY
        self.base_url = "https://accept.paymob.com/api"
        self.integration_id = settings.PAYMOB_INTEGRATION_ID

    def authenticate(self):
        """Get authentication token from Paymob"""
        url = f"{self.base_url}/auth/tokens"
        data = {"api_key": self.api_key}
        response = requests.post(url, json=data)
        return response.json().get("token")

    def register_order(self, amount_cents, order_id):
        """Register order with Paymob"""
        auth_token = self.authenticate()
        url = f"{self.base_url}/ecommerce/orders"
        data = {
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": amount_cents,
            "currency": "EGP",
            "merchant_order_id": order_id,
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_payment_key(self, amount_cents, order_id, billing_data):
        """Get payment key for the order"""
        order_response = self.register_order(amount_cents, order_id)
        auth_token = self.authenticate()
        url = f"{self.base_url}/acceptance/payment_keys"
        
        data = {
            "auth_token": auth_token,
            "amount_cents": amount_cents,
            "expiration": 3600,
            "order_id": order_response["id"],
            "billing_data": billing_data,
            "currency": "EGP",
            "integration_id": self.integration_id,
            "lock_order_when_paid": "false"
        }
        
        response = requests.post(url, json=data)
        return response.json().get("token")

def create_payment_session(order, request):
    """Create a payment session for an order"""
    paymob = PaymobAPI()
    
    # Convert order total to cents
    amount_cents = int(order.get_total_cost() * 100)
    
    # Prepare billing data
    billing_data = {
        "apartment": "NA",
        "email": order.email,
        "floor": "NA",
        "first_name": order.first_name,
        "street": order.address,
        "building": "NA",
        "phone_number": order.phone,
        "shipping_method": "NA",
        "postal_code": order.postal_code,
        "city": order.city,
        "country": "EG",
        "last_name": order.last_name,
        "state": "NA"
    }
    
    # Get payment key
    payment_token = paymob.get_payment_key(amount_cents, order.id, billing_data)
    
    # Return the iframe URL
    return f"https://accept.paymob.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_token}"
