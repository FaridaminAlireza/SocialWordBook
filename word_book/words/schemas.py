from pydantic import BaseModel, ConfigDict


class Word(BaseModel):
    group_id: int
    word_name: str
    word_part_of_speech: str
    description: str | None = None
    tags: list[str]
    examples: list[str]


class WordResponse(BaseModel):
    group_id: int
    word_name: str
    word_part_of_speech: str
    user_id: int
    description: str
    tags: list[str]
    examples: list[str]

    model_config = ConfigDict(from_attributes=True)
