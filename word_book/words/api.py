from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import word_book.words.service
from configs.database import get_db
from word_book.users.crud import read_user
from word_book.users.service.authentication import get_current_user
from word_book.words import crud, schemas

router = APIRouter()


@router.post("/word/", tags=["Words"])
def create_word_api(
    word: schemas.Word,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    word_book.words.service.create_word(db, user_object.id, word)
    db.commit()


@router.get("/word/", tags=["Words"])
def read_word_api(
    word_key: Optional[str] = None,
    pos: Optional[str] = None,
    group_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    result = word_book.words.service.read_word(
        db, user_object.id, word_key, pos, group_id
    )
    return result


@router.put("/word/", tags=["Words"])
def update_word_api(
    word: schemas.Word,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    word_book.words.service.update_word(db, user_object.id, word)
    db.commit()


@router.delete("/word/", tags=["Words"])
def delete_word_api(
    word_key: str,
    pos: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    crud.delete_word(db, user_object.id, word_key, pos)
    db.commit()
