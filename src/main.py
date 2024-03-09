from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from ad.router import router as router_ad, router_report
from admin.router import router as router_admin
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from comment.router import router as router_comment
from config import REDIS_HOST, REDIS_PORT

app = FastAPI(
    title='Test Task'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth',
    tags=['Auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Auth'],
)

app.include_router(router_admin)
app.include_router(router_ad)
app.include_router(router_comment)
app.include_router(router_report)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:7788'],
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=[
        'Content-Type',
        'Set-Cookie',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin',
        'Authorization',
    ],
)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='test_task_cache')
