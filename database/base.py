from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass

int_pk = Annotated[int, mapped_column(primary_key=True)]

class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

