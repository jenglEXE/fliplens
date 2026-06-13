import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from backend.database import get_db
from backend.routers.users import get_current_user

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter()

PRICE_ID = 'price_1Thh5tKGXdkXGiMC1BANSUid'


@router.post('/subscribe')
def subscribe(current_user: str = Depends(get_current_user)):
    db = get_db()
    result = db.table('users').select('*').eq('email', current_user).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail='User not found')
    user = result.data[0]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': PRICE_ID,
                'quantity': 1,
            }],
            customer_email=user['email'],
            success_url='https://getfliplens.com/success',
            cancel_url='https://getfliplens.com/pricing',
            metadata={'user_id': str(user['id'])}
        )
        return {'checkout_url': session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/cancel')
def cancel(current_user: str = Depends(get_current_user)):
    db = get_db()
    result = db.table('subscriptions').select('*').eq('user_id',
        db.table('users').select('id').eq('email', current_user).execute().data[0]['id']    
    ).eq('status', 'active').execute()

    if not result.data:
        raise HTTPException(status_code=404, detail='No active subscription found')
    
    sub = result.data[0]
    try:
        stripe.Subscription.modify(
            sub['stripe_id'],
            cancel_at_period_end=True
        )
        db.table('subscriptions').update({'status': 'cancelling'}).eq('id', sub['id']).execute()
        return {'message': 'Subscription will cancel at end of billing period'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get('/status')
def status(current_user: str = Depends(get_current_user)):
    db = get_db()
    user_result = db.table('users').select('*').eq('email', current_user).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail='User not found')
    user = user_result.data[0]

    sub_result = db.table('subscriptions').select('*').eq('user_id', user['id']).execute()
    
    return{
        'tier': user['tier'],
        'subscription': sub_result.data[0] if sub_result.data else None
    }


@router.post('/webhook')
async def webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail='Invalid signature')

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session['customer_email']
        stripe_subscription_id = session['subscription']

        db = get_db()
        user_result = db.table('users').select('id').eq('email', user_email).execute()
        if not user_result.data:
            return {'status': 'user not found'}

        user_id = user_result.data[0]['id']

        db.table('subscriptions').insert({
            'user_id': user_id,
            'stripe_id': stripe_subscription_id,
            'status': 'active'
        }).execute()

        db.table('users').update({'tier': 'paid'}).eq('id', user_id).execute()

    return {'status': 'ok'}