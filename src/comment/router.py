from logger import logger

from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select

from ad.router import get_ad_by_id
from auth.base_config import current_user
from auth.models import User
from comment.models import comment_table, FieldsForSorting
from comment.schemas import CommentRead, CommentCreate
from database import get_async_session
from pagination import Pagination, PaginatedResponse
from sorter import Sorter
from tg_utils.bot import send_message_on_exception

router = APIRouter(
    prefix='/comment',
    tags=['Comments']
)


@router.get(
    '/',
    response_model=PaginatedResponse[CommentRead],
)
@send_message_on_exception
async def get_comments_by_ad_id(
    request: Request,
    ad_id: int,
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(),
    sort_by: str = FieldsForSorting.id,
):
    sorter = Sorter(FieldsForSorting, sort_by)

    # check that ad are existing
    await get_ad_by_id(session, ad_id)

    sorted_select = sorter.apply_sorting(
        table=comment_table,
        query=select(
            comment_table.c.id,
            comment_table.c.text,
            comment_table.c.created_at,
            User.email
        ).join(
            User, User.id == comment_table.c.author_id
        ).where(
            comment_table.c.ad_id == ad_id
        ),
    )

    result = await session.execute(sorted_select)

    comments = [
        CommentRead(
            id=comment_id,
            text=comment_text,
            created_at=comment_created_at,
            author_email=user_email,
        ) for comment_id, comment_text, comment_created_at, user_email in result.all()
    ]

    logger.info(f'Got {len(comments)} comments')

    return pagination.paginate_items(comments)


@router.post('/create')
@send_message_on_exception
async def create_comment(
    request: Request,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    comment: CommentCreate = Depends(CommentCreate),
):
    new_comment = comment_table.insert().values(
        text=comment.text,
        author_id=user.id,
        ad_id=comment.ad_id,
    )
    await session.execute(new_comment)
    await session.commit()

    logger.info('Created comment')

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete('/{comment_id}')
@send_message_on_exception
async def delete_comment(
    comment_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not user.if_admin:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content='You do not have enough permissions to perform this operation.',
        )

    cond = comment_table.c.id == comment_id

    result = await session.execute(
        select(comment_table).where(cond)
    )
    comment_to_delete = result.scalar_one_or_none()

    if not comment_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )

    await session.execute(
        delete(comment_table).where(cond)
    )
    await session.commit()

    logger.info(f'Comment {comment_id} deleted')

    return Response(status_code=status.HTTP_204_NO_CONTENT)
