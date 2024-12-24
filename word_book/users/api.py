from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from configs.database import get_db
from word_book.users import crud
from word_book.users.crud import read_user
from word_book.users.service.authentication import (admin_required,
                                                    authenticate_user,
                                                    create_access_token)

router = APIRouter()


@router.post("/user/", tags=["Users"])
def create_user_api(
    username: str,
    password: str,
    role: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    crud.create_user(db, username, password, role)
    db.commit()


@router.get("/user/", tags=["Users"])
def read_user_api(
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    users = crud.read_users(db)
    return users


@router.put("/user/", tags=["Users"])
def update_user_api(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    user_object = read_user(db, username=current_user["username"])

    update_result = crud.update_user_password(
        db, user_object.username, old_password, new_password
    )
    db.commit()
    return update_result


@router.delete("/user/", tags=["Users"])
def delete_user_api(
    username: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    crud.delete_user(db, username)
    db.commit()


@router.post("/token", tags=["Authentication"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
