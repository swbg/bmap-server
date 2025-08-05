from pydantic import BaseModel
from typing import Optional
from datetime import date

#TODO add Products Pydantic schema for consistency
# Pydantic for timestamps handeling 

class PlaceSchema(BaseModel):
    placeId: int
    lat: float
    lon: float
    placeName: str
    placeType: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None
    validUntil: Optional[date] = (
        None  
    )

    class Config:
        orm_mode = True


class EntrySchema(BaseModel):
    entryId: int
    placeId: int
    productId: int
    price: Optional[float] = None
    volume: Optional[float] = None
    vomFass: Optional[bool] = None
    validFrom: Optional[date] = None
    lastUpdate: Optional[date] = None
    validUntil: Optional[date] = None

    class Config:
        orm_mode = True
