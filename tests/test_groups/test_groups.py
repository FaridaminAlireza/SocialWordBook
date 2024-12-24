from tests import conftest
from word_book.groups.crud import (create_group, create_user_group,
                                   delete_group, delete_user_group,
                                   read_groups, read_user_groups, update_group)
from word_book.groups.models import Group, UserGroup
from word_book.users.crud import create_user
from word_book.words.models import WordKey


class TestGroup:
    test_group_name = "TestGroup"
    new_test_group_name = "NewTestGroup"

    def test_create_group(self, db_session):
        create_user(
            db_session,
            username="user_1",
            password="user_1_password",
            role="student",
        )

        create_group(db_session, 1, self.test_group_name)

        word_object = WordKey(word_name="w_1", word_part_of_speech="pos_1")
        db_session.commit()

        assert db_session.query(Group).count() == 1

        group_name = (
            db_session.query(Group.group_name)
            .filter(Group.group_name == self.test_group_name)
            .scalar()
        )
        assert group_name == self.test_group_name

    def test_create_user_group(self, db_session):
        create_user_group(db_session, 1, self.test_group_name)
        db_session.commit()
        user_groups = (
            db_session.query(Group)
            .join(UserGroup, onclause=Group.id == UserGroup.group_id)
            .with_entities(Group.group_name)
            .filter(UserGroup.user_id == 1)
            .all()
        )
        user_groups = [i[0] for i in user_groups]

        assert user_groups == [self.test_group_name]

    def test_read_user_group(self, db_session):
        user_groups = read_user_groups(db_session, 1)
        assert user_groups == [self.test_group_name]

    def test_read_groups(self, db_session):
        groups = read_groups(db_session, 1)
        assert set(groups) == {self.test_group_name}

    def test_update_group(self, db_session):
        update_group(
            db_session, 1, self.test_group_name, self.new_test_group_name
        )
        db_session.commit()
        groups = read_groups(db_session, 1)
        assert set(groups) == {self.new_test_group_name}

    def test_delete_group(self, db_session):
        delete_user_group(db_session, 1, 1)
        delete_group(db_session, 1, self.new_test_group_name)
        db_session.commit()
        groups = read_groups(db_session, 1)
        assert not groups
