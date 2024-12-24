from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.database import Base

from ..groups.models import UserGroup


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String)
    password = mapped_column(String)
    role = mapped_column(String)
    word_key: Mapped["WordKey"] = relationship("WordKey", back_populates="user")
    user_group: Mapped["UserGroup"] = relationship(
        "UserGroup", back_populates="user"
    )
