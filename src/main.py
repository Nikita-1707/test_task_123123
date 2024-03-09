from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserCreate, UserRead
from auth.constants import admin_role_id
from config import REDIS_HOST, REDIS_PORT
from database import get_async_session
from pages.router import router as router_pages
from ad.router import router as router_ad, report_router
from comment.router import router as router_comment

app = FastAPI(
    title='Test Task'
)

app.mount('/static', StaticFiles(directory='static'), name='static')

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

app.include_router(router_pages)
app.include_router(router_ad)
app.include_router(report_router)
app.include_router(router_comment)

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


@app.post('/admin')
async def add_user_to_admin(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role_id != admin_role_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have enough permissions to perform this operation.'
        )

    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    user_to_promote = result.one_or_none()

    if not user_to_promote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found.'
        )

    await session.execute(
        update(User).where(User.id == user_id).values(
            role_id=admin_role_id
        )
    )
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
