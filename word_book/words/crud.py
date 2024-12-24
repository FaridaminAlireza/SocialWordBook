from sqlalchemy.orm import Session

from word_book.words import models


def delete_word(
    db: Session, user_id: int, word_key: str, pos: str, group_id: int
):

    # delete in multiple steps.
    db.query(models.WordKey).filter(
        models.WordKey.word_name == word_key,
        models.WordKey.word_part_of_speech == pos,
        models.WordKey.user_id == user_id,
        models.WordKey.group_id == group_id,
    ).update({models.WordKey.is_active: False}, synchronize_session="fetch")
