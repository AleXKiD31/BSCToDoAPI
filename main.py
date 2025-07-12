import json
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Request
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
root_database = os.path.join(os.path.dirname(__file__), 'database.json')
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
async def delete_todo(request:Request,id:str):
    with open(root_database) as f:
        data=json.load(f)
    del data[id]
    with open(root_database,'w') as f:
        json.dump(data,f)
    return RedirectResponse("/",303)

# Add new item to the list
@app.post("/add")
async def add_todo(request:Request):
    with open(root_database) as f:
        data=json.load(f)
    formdata=await request.form()
    newdata={}
    i=1
    for id in data:
        newdata[str(i)]=data[id]
        i+=1
    newdata[str(i)]=formdata["newtodo"]
    print(newdata)
    with open(root_database,'w') as f:
        json.dump(newdata,f)
    return RedirectResponse("/",303)