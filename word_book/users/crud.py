from sqlalchemy.orm import Session

from word_book.users import models
from word_book.users.service.authentication import (ALGORITHM, SECRET_KEY,
                                                    hash_password,
                                                    oauth2_scheme,
                                                    verify_password)


def read_users(session: Session):
    return session.query(models.User).all()


def read_user(session: Session, username: str):
    return (
        session.query(models.User)
        .filter(models.User.username == username)
        .one_or_none()
    )


def create_user(session: Session, username, password, role):
    hashed_password = hash_password(password)
    new_user = models.User(
        username=username, password=hashed_password, role=role
    )
    session.add(new_user)


def delete_user(session: Session, username):
    users_to_delete = (
        session.query(models.User)
        .filter(models.User.username == username)
        .all()
    )
    for user in users_to_delete:
        session.delete(user)


def update_user_password(db: Session, username, old_password, new_password):
    # verify current password
    # create hashed_password

    old_hashed_password = (
        db.query(models.User.password)
        .filter(models.User.username == username)
        .scalar()
    )

    if not old_hashed_password or not verify_password(
        old_password, old_hashed_password
    ):
        print("Wrong Username or Password!")
        return "Wrong Username or Password!"

    new_hashed_password = hash_password(new_password)
    db.query(models.User).filter(models.User.username == username).update(
        {models.User.password: new_hashed_password}, synchronize_session="fetch"
    )
