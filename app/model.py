from app.database import Base
from sqlalchemy import Column , Integer , String , Boolean,TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped , mapped_column, relationship
from sqlalchemy.sql.expression import text
from datetime import time

class Post(Base):
    __tablename__ = "post"

    id  : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    content : Mapped[str] = mapped_column(String, nullable=False)
    published : Mapped[bool] = mapped_column(Boolean, server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id : Mapped[int] = mapped_column(Integer , ForeignKey("user.id", ondelete="CASCADE") , nullable=False ) 
    owner = relationship("User", lazy="selectin")
    
 
class User(Base):
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(Integer,primary_key=True, nullable=True)
    email : Mapped[str] = mapped_column(String,nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    


# class Vote(Base):
#     __tablename__ = "votes"

#     user_id : Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE") ,primary_key=True)
#     post_id : Mapped[int] = mapped_column(Integer, ForeignKey("post.id", ondelete="CASCADE") ,primary_key=True)
   