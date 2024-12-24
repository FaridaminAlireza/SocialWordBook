from tests import conftest
from word_book.groups.crud import create_group
from word_book.users.crud import (create_user, delete_user, read_user,
                                  update_user_password)
from word_book.words.crud import delete_word
from word_book.words.models import (ListItem, Tag, WordContent,
                                    WordContentList, WordContentTag, WordKey)
from word_book.words.schemas import Word
from word_book.words.service import create_word, read_word, update_word


def test_create_word(db_session):

    create_user(
        db_session,
        username="user_1",
        password="user_1_password",
        role="student",
    )

    create_group(db_session, 1, "TestGroup")

    db_session.commit()

    new_word = Word(
        **{
            "group_id": 1,
            "word_name": "w_1",
            "word_part_of_speech": "pos_1",
            "description": "description_1",
            "tags": ["tag_1"],
            "examples": ["example_1", "example_2"],
        }
    )

    create_word(db_session, 1, new_word)
    db_session.commit()

    created_word = (
        db_session.query(WordKey.word_name)
        .filter(
            WordKey.word_name == "w_1", WordKey.word_part_of_speech == "pos_1"
        )
        .scalar()
    )
    assert created_word == "w_1"


def test_read_word(db_session):
    word = read_word(db_session, 1, "w_1", "pos_1", 1)
    assert word[0].word_name == "w_1"


def test_update_word(db_session):
    updated_word = Word(
        **{
            "group_id": 1,
            "word_name": "w_1",
            "word_part_of_speech": "pos_1",
            "description": "description_1",
            "tags": ["tag_1"],
            "examples": ["example_1", "example_2", "example3"],
        }
    )
    update_word(db_session, 1, updated_word)
    db_session.commit()
    word = read_word(db_session, 1, "w_1", "pos_1", 1)
    assert set(word[0].examples) == {"example_1", "example_2", "example3"}


def test_delete_word(db_session):
    delete_word(db_session, 1, "w_1", "pos_1", 1)
    db_session.commit()
    word = read_word(db_session, 1, "w_1", "pos_1", 1)
    assert not word
