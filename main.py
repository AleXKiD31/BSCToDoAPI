import json
from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}


# Get item
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Edit item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# Add new item to the list
@app.post("/add")
async def add_todo(request:Request):
    with open('database.json') as f:
        data=json.load(f)
    formdata=await request.form()
    newdata={}
    i=1
    for id in data:
        newdata[str(i)]=data[id]
        i+=1
    newdata[str(i)]=formdata["newtodo"]
    print(newdata)
    with open('database.json','w') as f:
        json.dump(newdata,f)
    return RedirectResponse("/",303)