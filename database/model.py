from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List
from sqlalchemy import Column,BIGINT,Boolean,DateTime,Integer,SmallInteger,String,text
from .base import Base, TableNameMixin


# Define your User and Queue classes
class User(Base, TableNameMixin):
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    premium: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    bonus_count: Mapped[int] = mapped_column(SmallInteger, server_default=text("0"))
    gender: Mapped[str] = mapped_column(String(1))
    pgender: Mapped[str] = mapped_column(String(1), server_default=text("'U'"))
    age: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    min_age: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    max_age: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    chat_count: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    lang: Mapped[str] = mapped_column(String(3), server_default=text("'en'"))
    country: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    interest : Mapped[Optional[str]] = mapped_column(String(10), server_default=text("'en'"))
    partner_id: Mapped[int] = mapped_column(BIGINT, nullable=True)
    previous_id: Mapped[int] = mapped_column(BIGINT, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, server_default=text("CURRENT_DATE"))
    banned: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    ban_expiry: Mapped[Optional[datetime]]= Column(DateTime, nullable=True)
    can_use: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    vip_expiry: Mapped[Optional[datetime]]= Column(DateTime, nullable=True)
    last_used:Mapped[Optional[datetime]]= Column(DateTime, nullable=True)
    reopen: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    request: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    


    def __repr__(self):
        return f"<User {self.user_id}>"


class Queue(Base, TableNameMixin):
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )



