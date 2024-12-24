from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.database import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(String)

    user_group: Mapped["UserGroup"] = relationship(
        "UserGroup", back_populates="group"
    )


class UserGroup(Base):
    __tablename__ = "users_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="user_group")
    group: Mapped["Group"] = relationship("Group", back_populates="user_group")
