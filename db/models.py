"""Models for the database.
"""
import datetime
from typing import Optional

from sqlalchemy import String, DateTime, LargeBinary, Float

from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# based on this tutorial:
# https://github.com/shayanfazeli/sqlalchemy_and_alembic_tutorial/blob/master/tutorial.ipynb


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "document_base"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    page_content: Mapped[Optional[str]]
    # dump: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    url: Mapped[Optional[str]] = mapped_column(String(255))
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}"

