from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Example(Base):
    __tablename__ = "example"
    __table_args__ = ()

    id = Column(Integer, autoincrement=True, primary_key=True)
    # goon and create columns
