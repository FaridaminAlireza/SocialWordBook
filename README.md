# WORDBOOK
The aim of this project is to provide a personalized 
language dictionary within the context of social circles.

This will aid langauge learners to:
- Engage actively in recording and reviewing new words
- Learn from other users of community.


In the context of a language class, this can help students to
learn from each other and aid teachers to keep track of 
students' progress in improving their vocabulary.

## Functionalities
*  Join a group
*  View the list of words added by other group members (Filterable by tag name)
*  Add words along with description and examples
*  Give tags to a word
*  View the list of added words (filterable by tag name)
*  Update or delete a word

## Architecture
  Model-Service-Controller
  * Model
    * Implemented as models.py
    *  Interacts with database through Object–relational mapping
  * Controller
    * Implemented as api.py
    * Directs client requests to Services
    * Also known as Router in Fastapi
    *  Request/Response data is validated with Pydantic
    *  Pydantic validation is implemented as schema.py
  * Service
    * Implemented as service.py
    * Holds the main business logic
    * Interacts with database through CRUD abstraction


## Implementation Tools
* Python
  * FastAPI
  * SQLAlchemy ORM
  * Pydantic Validation
  * Jose Authentication
  * Pytest
* Database
  * Postgresql
  * Alembic migration

