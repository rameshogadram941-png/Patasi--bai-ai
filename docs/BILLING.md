# Billing integration and manual UPI instructions for Patasi--bai‑ai

This document explains how the Stripe Checkout integration is wired and how to add the manual Google Pay / UPI contact to the landing page.

Manual Google Pay / UPI (fast)
- Displayed on the landing page: UPI / Google Pay number: 9901602603
- Ask payers to include a reference (email or company name) so the payment can be reconciled.

Stripe integration (recommended for production)
- Add these GitHub repository secrets (do NOT commit keys):
  - STRIPE_SECRET_KEY: your Stripe secret key (sk_test_... or sk_live_...)
  - STRIPE_PUBLISHABLE_KEY: your Stripe publishable key (pk_test_...)
  - STRIPE_WEBHOOK_SECRET: the webhook signing secret from Stripe for the payments webhook
  - STRIPE_SUCCESS_URL (optional): where to redirect on success
  - STRIPE_CANCEL_URL (optional): where to redirect on cancel

Files added
- web/landing/index.html — landing page with manual UPI block and a Stripe checkout button that calls /api/v1/payments/create-checkout-session
- app/payments/stripe_client.py — small wrapper around the Stripe SDK for creating Checkout sessions and verifying webhooks
- app/routes/payments.py — FastAPI routes: POST /api/v1/payments/create-checkout-session and POST /api/v1/payments/webhook

How to test locally (Stripe test mode)
1. Set test keys locally:
   export STRIPE_SECRET_KEY="sk_test_..."
   export STRIPE_PUBLISHABLE_KEY="pk_test_..."
   export STRIPE_WEBHOOK_SECRET="whsec_..."  # only needed when testing webhook signature verification
   export STRIPE_SUCCESS_URL="http://localhost:8000/success"
   export STRIPE_CANCEL_URL="http://localhost:8000/cancel"

2. Run the app locally and open the landing page:
   uvicorn app.main_app:app --reload --port 8000
   open http://localhost:8000/

3. Click Checkout to create a Stripe Checkout session (test mode). Use Stripe test cards or the Google Pay test wallet on supported devices.

4. To test webhooks locally, use the Stripe CLI to forward events:
   stripe listen --forward-to localhost:8000/api/v1/payments/webhook

Security and reconciliation
- The webhook handler verifies signatures using STRIPE_WEBHOOK_SECRET. Configure the webhook endpoint in your Stripe dashboard and copy the signing secret as a repo secret.
- On checkout completion the webhook should record payments in your billing DB and provision pilot/trial access. The current scaffold logs the event; implement DB writes and user provisioning per your flow.

Notes
- For India-first payments and native UPI experiences you can integrate Razorpay later — I can scaffold this on request.
