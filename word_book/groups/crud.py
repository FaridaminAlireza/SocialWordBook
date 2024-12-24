from sqlalchemy.orm import Session

from word_book.groups import models
from word_book.users import models as users_models


def create_group(db: Session, user_id: int, group_name: str) -> None:
    new_group = models.Group(group_name=group_name)
    db.add(new_group)
    db.flush()


def read_groups(db: Session, user_id: int) -> list[str]:
    group_names = db.query(models.Group.group_name).all()

    return [i[0] for i in group_names]


def update_group(
    db: Session, user_id: int, old_group_name: str, new_group_name: str
) -> None:
    group_object = (
        db.query(models.Group)
        .filter(models.Group.group_name == old_group_name)
        .one_or_none()
    )
    if not group_object:
        return
    group_object.group_name = new_group_name


def delete_group(db: Session, user_id: int, group_name: str) -> None:
    deleting_group = (
        db.query(models.Group)
        .filter(models.Group.group_name == group_name)
        .one_or_none()
    )
    if not deleting_group:
        return
    db.delete(deleting_group)


def create_user_group(db: Session, user_id, group_name) -> None:
    group_id = (
        db.query(models.Group.id)
        .filter(models.Group.group_name == group_name)
        .scalar()
    )
    if not group_id:
        return
    user_group_object = models.UserGroup(user_id=user_id, group_id=group_id)
    db.add(user_group_object)


def read_user_groups(db: Session, user_id: int) -> list[str]:
    group_names = (
        db.query(models.Group)
        .join(
            models.UserGroup,
            onclause=models.Group.id == models.UserGroup.group_id,
        )
        .join(
            users_models.User,
            onclause=models.UserGroup.user_id == users_models.User.id,
        )
        .with_entities(models.Group.group_name)
        .all()
    )

    return [i[0] for i in group_names]


def delete_user_group(db: Session, user_id, group_id) -> None:

    deleting_user_group = (
        db.query(models.UserGroup)
        .filter(
            models.UserGroup.group_id == group_id,
            models.UserGroup.user_id == user_id,
        )
        .one_or_none()
    )
    if not deleting_user_group:
        return
    db.delete(deleting_user_group)
