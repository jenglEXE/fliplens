from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import search, users, subscriptions
from backend.cache import clear_expired
import asyncio

app = FastAPI(
    title='FlipLens API',
    description='Cross-marketplace price research tool for professional resellers',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(search.router, prefix='/search', tags=['search'])
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(subscriptions.router, prefix='/subscriptions', tags=['subscriptions'])


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(cache_cleanup_task())


async def cache_cleanup_task():
    while True:
        await asyncio.sleep(300) #every 5 minutes
        clear_expired()


@app.get('/')
def root():
    return {'status': 'FlipLens API is running'}