from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import SessionLocal
from models import ToDoList
import os

app = FastAPI()

# Routes
root_template = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BSCToDoList'))
root_static = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BSCToDoList', 'static'))
templates=Jinja2Templates(directory=root_template)

app.mount(
    "/static",
    StaticFiles(directory=root_static),
    name="static",
)

# Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get item from table todo_list
# Return the item to todolist.html
@app.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    items = db.query(ToDoList).all()
    return templates.TemplateResponse('todolist.html',{"request":request,"tododict":items})

# Delete item from the list
@app.get("/delete/{id}")
async def delete_todo(id: int, db: Session = Depends(get_db)):
    todo_item = db.query(ToDoList).filter(ToDoList.id == id).first()

    # Exception when cant find item
    if not todo_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    db.delete(todo_item)
    db.commit()

    return RedirectResponse("/", status_code=303)

# Add new item to the list
@app.post("/add")
async def add_todo(request:Request, text_todo: str = Form(...), db: Session = Depends(get_db)):
    new_item = ToDoList(text_todo=text_todo)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return RedirectResponse("/",303)