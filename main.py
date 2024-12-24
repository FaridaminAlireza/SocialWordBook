from fastapi import APIRouter, FastAPI

from configs.database import create_all_tables
from word_book.groups.api import router as groups_router
from word_book.users.api import router as users_router
from word_book.words.api import router as words_router

default_router = APIRouter()


@default_router.get("/", tags=["Default"])
async def app_name():
    return "Welcome to WORDBOOK!"


app = FastAPI()

# Include the routers for each feature
app.include_router(default_router)
app.include_router(users_router)
app.include_router(groups_router)
app.include_router(words_router)
