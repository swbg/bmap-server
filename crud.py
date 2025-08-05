from math import isnan
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Product, Place, Entry


def clean_nan(
    place: Place, keys
) -> dict:  # TODO - add this to onboarding notebook and move to post after
    data = place.__dict__.copy()
    for key in keys:
        val = data.get(key)
        if val is not None and isinstance(val, float) and isnan(val):
            data[key] = None  # or 0.0, depending on your logic
    return data


# ------------------------------ PLACES ------------------------------


async def get_all_places(db: AsyncSession):
    result = await db.execute(select(Place))
    places = result.scalars().all()
    cleaned_places = [clean_nan(p, ["lat", "lon"]) for p in places]
    return cleaned_places


# Get place by ID
async def get_place_by_id(db: AsyncSession, place_id: int):
    result = await db.execute(select(Place).where(Place.placeId == place_id))
    return result.scalars().first()


# Create or update place
async def upsert_place(db: AsyncSession, place_data: dict):
    place_id = place_data.placeId

    if place_id is None:
        raise ValueError("placeId is required.")

    result = await db.execute(select(Place).where(Place.placeId == place_id))
    existing_place = result.scalars().first()

    if existing_place:
        for key, value in place_data.dict().items():
            setattr(existing_place, key, value)
        db.add(existing_place)
    else:
        new_place = Place(**place_data.dict())
        db.add(new_place)

    await db.commit()


# ------------------------------ PRODUCTS ------------------------------


async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.productId == product_id))
    return result.scalars().first()


async def upsert_product(db: AsyncSession, product_data: dict):
    product_id = product_data.get("productId")
    if product_id is None:
        raise ValueError("productId is required.")

    result = await db.execute(select(Product).where(Product.productId == product_id))
    existing_product = result.scalars().first()

    if existing_product:
        # Update fields
        for key, value in product_data.items():
            setattr(existing_product, key, value)
        db.add(existing_product)
    else:
        new_product = Product(**product_data)
        db.add(new_product)

    await db.commit()


# ------------------------------ ENTRIES ------------------------------


async def get_all_entries(db: AsyncSession):
    places = await db.execute(select(Entry))
    places = places.scalars().all()
    cleaned_places = [
        clean_nan(p, ["price", "volume"]) for p in places
    ]  # TODO remove hardcoded strings, improve preprocess
    return cleaned_places


async def get_entry_by_id(db: AsyncSession, entry_id: int):
    result = await db.execute(select(Entry).where(Entry.entryId == entry_id))
    return result.scalars().first()


async def create_entry(db: AsyncSession, entry_data: dict):
    entry_data = entry_data.dict()
    new_product = Entry(**entry_data)
    db.add(new_product)
    await db.commit()
