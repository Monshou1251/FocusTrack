# app/db/base.py
from types import MappingProxyType

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

NAMING_CONVENTIONS = MappingProxyType(
    {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

metadata = MetaData(naming_convention=NAMING_CONVENTIONS)
Base = declarative_base(metadata=metadata)
