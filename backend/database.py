from sqlmodel import SQLModel, Session, create_engine
import os

sqlite_file_name = "toolbox.db"
base_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_path = os.path.join(base_dir, sqlite_file_name)
sqlite_url = f"sqlite:///{sqlite_path}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    from models import User, RegexFavorite, PaletteFavorite, QuoteFavorite, DataFavorite 
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
