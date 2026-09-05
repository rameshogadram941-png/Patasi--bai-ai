import os
import stripe
from typing import Dict, Any, Optional

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

SUCCESS_URL = os.environ.get('STRIPE_SUCCESS_URL', 'https://example.com/success')
CANCEL_URL = os.environ.get('STRIPE_CANCEL_URL', 'https://example.com/cancel')

class StripeClient:
    def __init__(self, secret_key: Optional[str] = None):
        self._key = secret_key or stripe.api_key
        if not self._key:
            raise RuntimeError('STRIPE_SECRET_KEY not configured')
        stripe.api_key = self._key

    def create_checkout_session(self, price_cents: int = 10000, currency: str = 'inr', metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a Stripe Checkout session for a one-time payment.
        price_cents: amount in cents/paise depending on currency (e.g. 10000 = ₹100.00 if using INR smallest unit)
        """
        metadata = metadata or {}
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Patasi–bai‑ai Pilot / Payment',
                    },
                    'unit_amount': price_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=CANCEL_URL,
            metadata=metadata,
        )
        return session

    def construct_event(self, payload: bytes, sig_header: str, webhook_secret: str) -> Dict[str, Any]:
        return stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
