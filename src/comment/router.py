from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select

from ad.router import get_ad_by_id
from auth.base_config import current_user
from auth.models import User
from auth.utils import admin_role_id
from comment.models import comment_table
from comment.schemas import CommentRead, CommentCreate
from database import get_async_session
from pagination import Pagination, PaginatedResponse

router = APIRouter(
    prefix='/comment',
    tags=['Comments']
)


@router.get(
    '/',
    response_model=PaginatedResponse[CommentRead],
)
async def get_comments_by_ad_id(
    request: Request,
    ad_id: int,
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(),
):
    # check that ad are existing
    await get_ad_by_id(session, ad_id)

    result = await session.execute(
        select(
            comment_table.c.id,
            comment_table.c.text,
            comment_table.c.created_at,
            User.email
        ).join(User, User.id == comment_table.c.author_id).where(comment_table.c.ad_id == ad_id)
    )

    comments = [
        CommentRead(
            id=comment_id,
            text=comment_text,
            created_at=comment_created_at,
            author_email=user_email,
        ) for comment_id, comment_text, comment_created_at, user_email in result.all()
    ]

    return pagination.paginate_items(comments)


@router.post('/create')
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

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete('/{comment_id}')
async def delete_comment(
    comment_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role_id != admin_role_id:
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

    return Response(status_code=status.HTTP_204_NO_CONTENT)
