from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    id: int
    name: str


# shortcut: in-memory store, replace with a real database before production
_items: dict[int, Item] = {}


@router.get("/items")
def list_items() -> list[Item]:
    return list(_items.values())


@router.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="item not found")
    return _items[item_id]


@router.post("/items", status_code=201)
def create_item(item: Item) -> Item:
    if item.id in _items:
        raise HTTPException(status_code=409, detail="item exists")
    _items[item.id] = item
    return item
