from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./relax.db"
engine = create_engine(DATABASE_URL, echo=False)
