from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    pub_date = Column(DateTime)
    headline = Column(String)
    content = Column(String)
    # external_id = relationship("ExternalId", back_populates="article")


class ExternalId(Base):
    __tablename__ = "external_ids"
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
