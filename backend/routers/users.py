from fastapi import APIRouter

router = APIRouter()


@router.post('/register')
def register():
    return {'message': 'register endpoint coming soon'}


@router.post('/login')
def login():
    return {'message': 'me endpoint coming soon'}