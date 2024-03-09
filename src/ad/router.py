from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, true

from ad.models import ad_table, AdFieldsForSorting, report_table, ReportFieldsForSorting
from ad.schemas import AdRead, AdCreate, AdTypeEnum, ReportCreate, ReportRead
from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from pagination import Pagination, PaginatedResponse
from sorter import Sorter

router = APIRouter(
    prefix='/ad',
    tags=['Ads']
)

report_router = APIRouter(
    prefix='/report',
    tags=['Reports']
)


async def get_ad_by_id(
    session: AsyncSession,
    ad_id: int,
) -> AdRead:
    result = await session.execute(
        select(ad_table).where(ad_table.c.id == ad_id)
    )

    ad = result.one_or_none()

    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ad not found',
        )

    return AdRead(
        id=ad.id,
        title=ad.title,
        description=ad.description,
    )


@router.get(
    '/',
    response_model=PaginatedResponse[AdRead],
)
async def get_all_ads(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(),
    ad_type: AdTypeEnum = '',
    sort_by: str = AdFieldsForSorting.id,
):
    sorter = Sorter(AdFieldsForSorting, sort_by)

    cond = ad_table.c.type == ad_type if ad_type else true()

    result = await session.execute(
        sorter.apply_sorting(
            query=select(ad_table).where(cond),
            table=ad_table,
        )
    )
    ads = [
        AdRead(
            id=ad.id,
            title=ad.title,
            description=ad.description,
        ) for ad in result.all()
    ]

    return pagination.paginate_items(ads)


@router.get(
    '/{ad_id}',
    response_model=AdRead,
)
async def get_ad(
    request: Request,
    ad_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return get_ad_by_id(session, ad_id)


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

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete('/{ad_id}')
async def delete_ad(
    ad_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    cond = ad_table.c.id == ad_id

    result = await session.execute(
        select(ad_table).where(cond)
    )
    ad_to_delete = result.one_or_none()

    if not ad_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ad not found'
        )

    if (
        not user.if_admin
        and ad_to_delete.author_id != user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have enough permissions to perform this operation',
        )

    await session.execute(
        delete(ad_table).where(cond)
    )
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@report_router.post('/create')
async def create_report(
    request: Request,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    report: ReportCreate = Depends(ReportCreate),
):
    # check that ad are existing
    await get_ad_by_id(session, report.ad_id)

    new_ad = report_table.insert().values(
        message=report.message,
        reporter_id=user.id,
        ad_id=report.ad_id,
    )
    await session.execute(new_ad)
    await session.commit()

    return Response(status_code=status.HTTP_201_CREATED)


@report_router.get('/{ad_id}')
async def get_reports_by_ad_id(
    request: Request,
    ad_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(),
    sort_by: str = ReportFieldsForSorting.id,
):
    if not user.if_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have enough permissions to perform this operation.',
        )

    sorter = Sorter(ReportFieldsForSorting, sort_by)

    # check that ad are existing
    await get_ad_by_id(session, ad_id)

    result = await session.execute(
        sorter.apply_sorting(
            table=report_table,
            query=select(report_table).where(
                report_table.c.ad_id == ad_id
            ),
        )
    )

    reports = [
        ReportRead(
            id=report.id,
            message=report.message,
            ad_id=report.ad_id,
            reporter_id=user.id,
        ) for report in result.all()
    ]

    return pagination.paginate_items(reports)
