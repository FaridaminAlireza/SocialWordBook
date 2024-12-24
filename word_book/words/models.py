from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.database import Base


class WordKey(Base):
    __tablename__ = "word_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    word_name: Mapped[str] = mapped_column(String)
    word_part_of_speech: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user: Mapped["User"] = relationship("User", back_populates="word_key")


class WordContent(Base):
    __tablename__ = "word_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_key_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("word_keys.id", ondelete="CASCADE")
    )

    description: Mapped["str"] = mapped_column(String)

    word_content_tag: Mapped["WordContentTag"] = relationship(
        "WordContentTag", back_populates="word_content"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag: Mapped[str] = mapped_column(String)

    word_content_tag: Mapped["WordContentTag"] = relationship(
        "WordContentTag", back_populates="tag"
    )


class WordContentTag(Base):
    __tablename__ = "word_contents_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    word_content_id: Mapped[int] = mapped_column(ForeignKey("word_contents.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    tag: Mapped["Tag"] = relationship("Tag", back_populates="word_content_tag")
    word_content: Mapped["WordContent"] = relationship(
        "WordContent", back_populates="word_content_tag"
    )


class WordContentList(Base):
    __tablename__ = "word_contents_lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_content_id: Mapped[int] = mapped_column(
        ForeignKey("word_contents.id", ondelete="CASCADE")
    )


class ListItem(Base):
    __tablename__ = "word_contents_lists_items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    item_data: Mapped[str] = mapped_column(String)
    item_type: Mapped[str] = mapped_column(String)

    word_content_list_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("word_contents_lists.id", ondelete="CASCADE"),
        nullable=False,
    )
