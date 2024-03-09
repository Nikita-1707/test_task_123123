from typing import Generic, TypeVar, List

from fastapi import Query
from pydantic.generics import GenericModel

T = TypeVar('T')


class PaginatedResponse(GenericModel, Generic[T]):
    page_number: int
    pages_count: int
    count: int
    offset: int
    data: List[T]


class Pagination:

    def __init__(
        self,
        page_size: int = Query(10, alias='page_size'),
        offset: int = Query(0, alias='offset'),
    ):
        self.page_size = page_size
        self.offset = offset

    def paginate_items(
        self,
        items: List[T],
    ) -> PaginatedResponse[T]:
        total_count = len(items)
        paginated_items = items[self.offset:self.offset + self.page_size]
        pages_count = (total_count + self.page_size - 1) // self.page_size

        return PaginatedResponse[T](
            page_number=(self.offset // self.page_size) + 1,
            pages_count=pages_count,
            count=total_count,
            offset=self.offset,
            data=paginated_items
        )
