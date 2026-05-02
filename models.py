from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String)
    category = Column(String, index=True, default="Général")