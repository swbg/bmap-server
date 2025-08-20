from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from crud import (
    create_entry,
    get_all_entries,
    get_all_places,
    get_all_products,
    get_entry_by_id,
    get_place_by_id,
    get_product_by_id,
    upsert_place,
    upsert_product,
)
from schema import EntrySchema, PlaceSchema, ProductSchema

# ----------------------------- API Config -----------------------------


DATABASE_URL = "sqlite+aiosqlite:///./data/main.db"

# Create engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db():
    async with async_session() as session:
        yield session


app = FastAPI()

origins = [
    "http://kurze-durststrecke.de",
    "http://localhost:5432",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ------------------------------ API Endpoints ----------------------------
# -------------------------------- PRODUCTS -------------------------------


# Get all products
@app.get("/products")
async def products(db: AsyncSession = Depends(get_db)):
    return await get_all_products(db)


# Get one product by id
@app.get("/products/{product_id}")
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Inser or upsert new product
# Test: {"brand_name": "TESTNAME","product_name": "TESTNAME","product_type": "TESTTYPE"}
@app.post("/products")
async def create_or_update_product(
    product: ProductSchema, db: AsyncSession = Depends(get_db)
):
    try:
        await upsert_product(db, product)
        return {"message": "Product created or updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------- PLACES -------------------------------


# Get all places
@app.get("/places", response_model=List[PlaceSchema])
async def read_places(db: AsyncSession = Depends(get_db)):
    return await get_all_places(db)


# Get one place by id
@app.get("/places/{place_id}")
async def read_place(place_id: int, db: AsyncSession = Depends(get_db)):
    place = await get_place_by_id(db, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


# Inser or upsert new place
# Test: {"lat": 10.000, "lon": 1.000, "place_name": "TestName", "place_type": "TestType", "address": "Testweg", "website": "http://test.de", "phone": "+123", "note": "TestNote"}
@app.post("/places")
async def create_or_update_place(
    place: PlaceSchema, db: AsyncSession = Depends(get_db)
):
    print("Incoming data:", place)
    try:
        await upsert_place(db, place)
        return {"message": "Place created or updated"}
    except Exception as e:
        print("message", place)
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------- ENTIRES -------------------------------


# Get all entries
@app.get("/entries", response_model=List[EntrySchema])
async def read_entries(db: AsyncSession = Depends(get_db)):
    entries = await get_all_entries(db)
    return entries


# Get one entry by id
@app.get("/entries/{entry_id}")
async def read_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    entry = await get_entry_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


# Insert new entry
# Test { "entry_id":99999, "place_id": 9999, "product_id": 999, "price": 100, "volume": 0.5,"vom_fass": false, "valid_from": "2000-01-01", "last_update": "2005-01-01"}
@app.post("/entries")
async def create_new_entry(entry: EntrySchema, db: AsyncSession = Depends(get_db)):
    try:
        db_entry = await create_entry(db, entry)
        return db_entry
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Could not create entry: {str(e)}")
