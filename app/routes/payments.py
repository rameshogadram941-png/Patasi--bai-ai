from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import logging

from app.payments.stripe_client import StripeClient

router = APIRouter()
logger = logging.getLogger('patasi.payments')

stripe_client = None
try:
    stripe_client = StripeClient()
except Exception:
    # Stripe not configured yet; endpoints will return 500 until secret is provided
    stripe_client = None

@router.post('/api/v1/payments/create-checkout-session')
async def create_checkout():
    if not stripe_client:
        raise HTTPException(status_code=500, detail='Payment not configured')
    # For pilot quick-pay we use a default amount (₹500 as example). You can pass amount via body in future.
    session = stripe_client.create_checkout_session(price_cents=50000, currency='inr')
    return JSONResponse({'url': session.url})

@router.post('/api/v1/payments/webhook')
async def stripe_webhook(request: Request):
    # Verify and handle Stripe webhook events.
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    if not webhook_secret:
        raise HTTPException(status_code=500, detail='Webhook secret not configured')

    payload = await request.body()
    sig_header = request.headers.get('stripe-signature', '')
    try:
        event = stripe_client.construct_event(payload, sig_header, webhook_secret)
    except Exception as e:
        logger.exception('Webhook signature verification failed')
        raise HTTPException(status_code=400, detail='Invalid signature')

    # Handle relevant events (extend as needed)
    typ = event['type']
    logger.info('Stripe webhook received: %s', typ)

    if typ == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: record payment in DB, create billing record, provision trial access, send welcome email
        logger.info('Checkout completed: id=%s, customer=%s', session.get('id'), session.get('customer'))

    return JSONResponse({'status': 'ok'})
