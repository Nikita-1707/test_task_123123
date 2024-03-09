from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.constants import admin_role_id
from auth.models import User
from database import get_async_session

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.post('/{user_id}')
async def add_user_to_admin(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not user.if_admin:
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


@router.post('/{user_id}/ban')
async def ban_user(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await _change_user_is_active(
        new_is_active=False,
        user_id=user_id,
        user=user,
        session=session,
    )


@router.post('/{user_id}/unban')
async def unbun_user(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await _change_user_is_active(
        new_is_active=True,
        user_id=user_id,
        user=user,
        session=session,
    )


async def _change_user_is_active(
    new_is_active: bool,
    user_id: int,
    user: User,
    session: AsyncSession,
) -> Response:
    if not user.if_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have enough permissions to perform this operation.'
        )

    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    user_to_change = result.one_or_none()

    if not user_to_change:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} not found.'
        )

    await session.execute(
        update(User).where(User.id == user_id).values(
            is_active=new_is_active
        )
    )
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
