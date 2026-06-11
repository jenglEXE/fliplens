from fastapi import APIRouter

router = APIRouter()


@router.post('/subscribe')
def subscribe():
    return {'message': 'subscribe endpoint coming soon'}


@router.post('/cancel')
def cancel():
    return {'message': 'cancel endpoint coming soon'}


@router.get('/status')
def status():
    return {'message': 'status endpoint coming soon'}