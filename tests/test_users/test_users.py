from tests import conftest
from word_book.users.crud import (create_user, delete_user, read_user,
                                  update_user_password)
from word_book.users.models import User
from word_book.users.service.authentication import verify_password
from word_book.words.models import WordKey
from word_book.words.service import create_word


def test_create_user(db_session):
    create_user(
        db_session,
        username="user_1",
        password="user_1_password",
        role="student",
    )
    word_object = WordKey(word_name="w_1", word_part_of_speech="pos_1")
    db_session.commit()

    assert db_session.query(User).count() == 1
    new_user = (
        db_session.query(User)
        .filter(User.username == "user_1", User.role == "student")
        .one()
    )

    assert new_user.username == "user_1" and new_user.role == "student"


def test_read_user(db_session):
    new_user = read_user(db_session, username="user_1")

    assert new_user.username == "user_1" and new_user.role == "student"


def test_update_user(db_session):
    new_user = (
        db_session.query(User)
        .filter(User.username == "user_1", User.role == "student")
        .one()
    )
    assert new_user.username == "user_1" and new_user.role == "student"
    print(new_user.password)
    assert verify_password("user_1_password", new_user.password)
    update_user_password(
        db_session,
        username="user_1",
        old_password="user_1_password",
        new_password="user_1_new_password",
    )
    db_session.commit()
    db_session.refresh(new_user)
    assert verify_password("user_1_new_password", new_user.password)


def test_delete_user(db_session):
    new_user = (
        db_session.query(User)
        .filter(User.username == "user_1", User.role == "student")
        .one()
    )
    assert new_user.username == "user_1" and new_user.role == "student"

    delete_user(db_session, username=new_user.username)
    db_session.commit()

    new_user = (
        db_session.query(User)
        .filter(User.username == "user_1", User.role == "student")
        .one_or_none()
    )
    assert new_user is None
