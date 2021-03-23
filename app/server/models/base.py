from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, BOOLEAN
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

    deleted = Column("deleted", BOOLEAN, nullable=False, comment="論理削除フラグ")

    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment="登録日時",
    )

    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        onupdate=current_timestamp(),
        comment="最終更新日時",
    )

    @declared_attr
    def __mapper_args__(self):
        return {"order_by": "id"}
