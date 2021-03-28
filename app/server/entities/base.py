from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN, DATETIME
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.functions import current_timestamp
from database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    deleted = Column(BOOLEAN, nullable=False, comment="論理削除フラグ", default=False)

    created_at = Column(
        DATETIME(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment="登録日時",
    )

    updated_at = Column(
        DATETIME(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        onupdate=current_timestamp(),
        comment="最終更新日時",
    )

    @declared_attr
    def __mapper_args__(self):
        return {"order_by": "id"}
