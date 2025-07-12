from sqlalchemy import Column, Integer, String
from database import Base

class ToDoList(Base):
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True)
    text_todo = Column(String(255))
