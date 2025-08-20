from datetime import date
from typing import Optional

from pydantic import BaseModel

# Pydantic for timestamps handeling


class PlaceSchema(BaseModel):
    place_id: Optional[int] = None
    lat: float
    lon: float
    place_name: str
    place_type: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None
    valid_until: Optional[date] = None

    class Config:
        orm_mode = True


class EntrySchema(BaseModel):
    entry_id: Optional[int] = None
    place_id: int
    product_id: int
    price: Optional[float] = None
    volume: Optional[float] = None
    vom_fass: Optional[bool] = None
    valid_from: Optional[date] = None
    last_update: Optional[date] = None
    valid_until: Optional[date] = None

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    product_id: Optional[int] = None
    brand_name: Optional[str] = None
    product_name: str
    product_type: str

    class Config:
        orm_mode = True
