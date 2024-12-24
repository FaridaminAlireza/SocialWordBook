from collections import defaultdict

from sqlalchemy.orm import Session

from word_book.users import models as users_models
from word_book.words import models, schemas
from word_book.words.crud import delete_word


def create_word(db: Session, user_id: int, word: schemas.Word) -> None:

    word_name = word.word_name
    pos = word.word_part_of_speech
    tags = word.tags
    description = word.description
    examples = word.examples
    group_id = word.group_id

    existing_word_key_object = (
        db.query(models.WordKey)
        .filter(
            models.WordKey.word_name == word_name,
            models.WordKey.word_part_of_speech == pos,
            models.WordKey.user_id == user_id,
            models.WordKey.is_active == True,
            models.WordKey.group_id == group_id,
        )
        .one_or_none()
    )

    if existing_word_key_object:
        print("word_key already exists!")
        return

    word_key_object = models.WordKey(
        word_name=word_name,
        user_id=user_id,
        word_part_of_speech=pos,
        group_id=group_id,
    )
    db.add(word_key_object)
    db.flush()

    tag_ids = []
    available_tags = (
        db.query(models.Tag.tag).filter(models.Tag.tag.in_(tags)).all()
    )
    available_tags = [i[0] for i in available_tags]
    new_tags_to_add = tags
    if available_tags:
        new_tags_to_add = set(tags) - set(available_tags)
    for new_tag in new_tags_to_add:
        new_tag_objet = models.Tag(tag=new_tag)
        db.add(new_tag_objet)
    db.flush()

    tag_ids = db.query(models.Tag.id).filter(models.Tag.tag.in_(tags)).all()
    tag_ids = [i[0] for i in tag_ids]

    word_content_object = models.WordContent(
        word_key_id=word_key_object.id,
        description=description,
    )
    db.add(word_content_object)
    db.flush()

    new_list_object = models.WordContentList(
        word_content_id=word_content_object.id
    )
    db.add(new_list_object)
    db.flush()

    for tag_id in tag_ids:
        new_word_content_tag_object = models.WordContentTag(
            word_content_id=word_content_object.id, tag_id=tag_id
        )
        db.add(new_word_content_tag_object)
    db.flush()

    for example in examples:
        new_item_object = models.ListItem(
            word_content_list_id=new_list_object.id,
            item_data=example,
            item_type="example",
        )
        db.add(new_item_object)
    db.flush()


def read_word(
    db: Session,
    user_id: int,
    word_key: str = None,
    pos: str = None,
    group_id: int = None,
):

    query = (
        db.query(models.WordKey)
        .join(users_models.User, users_models.User.id == models.WordKey.user_id)
        .join(
            models.WordContent,
            models.WordContent.word_key_id == models.WordKey.id,
        )
        .join(
            models.WordContentTag,
            models.WordContentTag.word_content_id == models.WordContent.id,
        )
        .join(models.Tag, models.Tag.id == models.WordContentTag.tag_id)
        .join(
            models.WordContentList,
            models.WordContentList.word_content_id == models.WordContent.id,
        )
        .join(
            models.ListItem,
            models.ListItem.word_content_list_id == models.WordContentList.id,
        )
        .with_entities(
            models.WordKey.group_id,
            models.WordKey.word_name,
            models.WordKey.word_part_of_speech,
            models.WordKey.user_id,
            models.WordContent.description,
            models.Tag.tag,
            models.ListItem.id,
            models.ListItem.item_type,
            models.ListItem.item_data,
        )
    ).filter(
        models.WordKey.is_active == True, models.WordKey.user_id == user_id
    )

    if word_key and pos:
        query = query.filter(
            models.WordKey.word_name == word_key,
            models.WordKey.word_part_of_speech == pos,
        )

    if group_id:
        query = query.filter(
            models.WordKey.group_id == group_id,
        )

    results = [i._mapping for i in query.all()]

    words_dict = defaultdict(list)

    for i in results:
        words_dict[
            (
                i["word_name"],
                i["word_part_of_speech"],
                i["user_id"],
                i["group_id"],
            )
        ].append(i)

    tags = set()
    examples = set()

    if not results:
        return []

    word_list = []
    for (word_name, pos, user_id, group_id), results in words_dict.items():

        word_name = results[0]["word_name"]
        description = results[0]["description"]
        pos = results[0]["word_part_of_speech"]
        group_id = results[0]["group_id"]

        for result in results:
            tags.add(result["tag"])
            if result["item_type"] == "example":
                examples.add(result["item_data"])
        word_list.append(
            schemas.WordResponse(
                tags=list(tags),
                examples=list(examples),
                word_name=word_name,
                description=description,
                word_part_of_speech=pos,
                user_id=user_id,
                group_id=group_id,
            )
        )

    return word_list


def update_word(db: Session, user_id: int, word: schemas.Word):

    if read_word(db, user_id, word.word_name, word.word_part_of_speech):
        delete_word(
            db, user_id, word.word_name, word.word_part_of_speech, word.group_id
        )
        create_word(db, user_id, word)
    else:
        print("Error! the word does not exist!")
