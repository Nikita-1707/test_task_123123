from enum import Enum
from fastapi import Query
from sqlalchemy import desc, asc, Table
from sqlalchemy.sql import Selectable


class Sorter:
    def __init__(
        self,
        sorting_enum: (str, Enum),
        sort_by: str = Query('id', alias='sort_by'),
    ) -> None:
        self._sort_by = sort_by
        self._sorting_enum = sorting_enum

        self._sort_field = 'id'  # default sort field
        self._sort_descending = False

        self._extract_sort_by()

    def _extract_sort_by(self):
        if self._sort_by.startswith('-'):
            sort_field = self._sort_by[1:]
            self._sort_descending = True
        else:
            sort_field = self._sort_by

        # Validate the sort field
        if sort_field in self._sorting_enum.__members__:
            self._sort_field = sort_field
        else:
            self._sort_field = 'id'  # default to 'id' if invalid field

    def apply_sorting(
        self,
        query: Selectable,
        table: Table,
    ) -> Selectable:
        if self._sort_descending:
            return query.order_by(desc(getattr(table.c, self._sort_field)))
        else:
            return query.order_by(asc(getattr(table.c, self._sort_field)))
