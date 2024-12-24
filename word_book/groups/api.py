from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from configs.database import get_db
from word_book.groups import crud, schemas
from word_book.users.crud import read_user
from word_book.users.service.authentication import (admin_required,
                                                    get_current_user)

router = APIRouter()


@router.post("/group/", tags=["Groups"])
def create_group_api(
    group_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    user_object = read_user(db, username=current_user["username"])
    crud.create_group(db, user_object.id, group_name)
    db.commit()


@router.get("/group/", tags=["Groups"])
def read_group_api(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    result = crud.read_groups(db, user_object.id)
    return result


@router.put("/group/", tags=["Groups"])
def update_group_api(
    old_group_name: str,
    new_group_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    user_object = read_user(db, username=current_user["username"])
    crud.update_group(db, user_object.id, old_group_name, new_group_name)
    db.commit()


@router.delete("/group/", tags=["Groups"])
def delete_group_api(
    group_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    user_object = read_user(db, username=current_user["username"])
    crud.delete_group(db, user_object.id, group_name)
    db.commit()


@router.post("/group/user-group", tags=["Groups"])
def create_user_group_api(
    group_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    crud.create_user_group(db, user_object.id, group_name)
    db.commit()


@router.get("/group/user-group", tags=["Groups"])
def read_user_group_api(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    result = crud.read_user_groups(db, user_object.id)
    return result


@router.delete("/group/user-group", tags=["Groups"])
def read_user_group_api(
    group_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_object = read_user(db, username=current_user["username"])
    crud.delete_user_group(db, user_object.id, group_name)
    db.commit()
