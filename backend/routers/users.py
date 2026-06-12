from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email


@router.post('/register', response_model=Token)
def register(user: UserCreate):
    db = get_db()
    existing = db.table('users').select('id').eq('email', user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed = hash_password(user.password)
    db.table('users').insert({
        'email': user.email,
        'password_hash': hashed,
        'tier': 'free'
    }).execute()
    token = create_access_token({'sub': user.email})
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    result = db.table('users').select('*').eq('email', form_data.username).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    user = result.data[0]
    if not verify_password(form_data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': user['email']})
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/me')
def me(current_user: str = Depends (get_current_user)):
    db = get_db()
    result = db.table('users').select('id, email, tier, created_at').eq('email', current_user).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail='User not found')
    return result.data[0]