import strawberry
from strawberry.types import Info
from typing import List, Optional
import re
from models import Bookmark as BookmarkModel
from database import SessionLocal
from sqlalchemy.orm import Session

# Define the GraphQL type for Bookmark
@strawberry.type
class Bookmark:
    id: int
    name: str
    url: str
    category: str

# Helper to convert SQLAlchemy model to GraphQL type
def from_orm(bookmark: BookmarkModel) -> Bookmark:
    return Bookmark(
        id=bookmark.id,
        name=bookmark.name,
        url=bookmark.url,
        category=bookmark.category
    )

# Query class
@strawberry.type
class Query:
    @strawberry.field
    def bookmarks(self, info: Info, 
                  category: Optional[str] = None, 
                  search: Optional[str] = None,
                  skip: int = 0,
                  limit: int = 100) -> List[Bookmark]:
        db: Session = SessionLocal()
        try:
            query = db.query(BookmarkModel)
            if category:
                query = query.filter(BookmarkModel.category == category)
            if search:
                query = query.filter(
                    (BookmarkModel.name.ilike(f"%{search}%")) | 
                    (BookmarkModel.url.ilike(f"%{search}%"))
                )
            bookmarks = query.offset(skip).limit(limit).all()
            return [from_orm(b) for b in bookmarks]
        finally:
            db.close()

    @strawberry.field
    def bookmark(self, info: Info, id: int) -> Optional[Bookmark]:
        db: Session = SessionLocal()
        try:
            bookmark = db.query(BookmarkModel).filter(BookmarkModel.id == id).first()
            return from_orm(bookmark) if bookmark else None
        finally:
            db.close()

# Mutation class
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_bookmark(self, info: Info, name: str, url: str, category: str = "Général") -> Bookmark:
        # Validation URL basique côté backend
        url_pattern = re.compile(r'^https?://')
        if not url_pattern.match(url):
            raise Exception("URL invalide. Elle doit commencer par http:// ou https://")

        db: Session = SessionLocal()
        try:
            db_bookmark = BookmarkModel(name=name, url=url, category=category)
            db.add(db_bookmark)
            db.commit()
            db.refresh(db_bookmark)
            return from_orm(db_bookmark)
        finally:
            db.close()

    @strawberry.mutation
    def update_bookmark(self, info: Info, id: int, name: Optional[str] = None,
                        url: Optional[str] = None, category: Optional[str] = None) -> Optional[Bookmark]:
        db: Session = SessionLocal()
        try:
            db_bookmark = db.query(BookmarkModel).filter(BookmarkModel.id == id).first()
            if not db_bookmark:
                return None
            if name is not None:
                db_bookmark.name = name
            if url is not None:
                db_bookmark.url = url
            if category is not None:
                db_bookmark.category = category
            db.commit()
            db.refresh(db_bookmark)
            return from_orm(db_bookmark)
        finally:
            db.close()

    @strawberry.mutation
    def delete_bookmark(self, info: Info, id: int) -> bool:
        db: Session = SessionLocal()
        try:
            db_bookmark = db.query(BookmarkModel).filter(BookmarkModel.id == id).first()
            if not db_bookmark:
                return False
            db.delete(db_bookmark)
            db.commit()
            return True
        finally:
            db.close()

# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)