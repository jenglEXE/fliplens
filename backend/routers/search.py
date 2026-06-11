from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def search():
    return {'message': 'search endpoint coming soon'}


@router.get('/history')
def history():
    return {'message': 'history endpoint coming soon'}