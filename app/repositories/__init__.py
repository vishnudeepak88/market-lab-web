from app.repositories.db_repo import DBRepository
from app.repositories.mock_repo import MockRepository

def get_repository(db_session=None):
    if db_session:
        return DBRepository(db_session)
    return MockRepository()
