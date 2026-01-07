from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI(title="Mini Backend API")

# In-memory "database"
DB: Dict[int, dict] = {}
NEXT_ID = 1


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class Item(ItemCreate):
    id: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    global NEXT_ID

    new_item = item.model_dump()
    new_item["id"] = NEXT_ID
    DB[NEXT_ID] = new_item
    NEXT_ID += 1

    return new_item


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return DB[item_id]


@app.get("/items")
def list_items(limit: int = 10):
    # simple listing
    items = list(DB.values())[:limit]
    return {"count": len(items), "items": items}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    del DB[item_id]
    return {"message": "Deleted successfully"}
