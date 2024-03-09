from typing import List

from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ad.models import ad_table
from ad.schemas import AdRead, AdCreate
from auth.base_config import current_user
from auth.models import User
from database import get_async_session

router = APIRouter(
    prefix='/ad',
    tags=['Ads']
)


@router.get(
    '/',
    response_model=List[AdRead],
)
async def get_all_ads(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(ad_table)
    )
    return [
        AdRead(
            id=ad.id,
            title=ad.title,
            description=ad.description,
        ) for ad in result.all()
    ]


@router.get(
    '/{ad_id}',
    response_model=AdRead,
)
async def get_all_ads(
    request: Request,
    ad_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(ad_table).where(ad_table.c.id == ad_id)
    )

    ad = result.one_or_none()

    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found',
        )

    return AdRead(
        id=ad.id,
        title=ad.title,
        description=ad.description,
    )


@router.post('/create')
async def create_ad(
    request: Request,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    ad: AdCreate = Depends(AdCreate),
):
    new_ad = ad_table.insert().values(
        title=ad.title,
        description=ad.description,
        type=ad.type,
        author_id=user.id,
    )
    await session.execute(new_ad)
    await session.commit()

    return 'Ad created successfully'
