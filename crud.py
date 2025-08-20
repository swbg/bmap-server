from math import isnan
from typing import Sequence, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Entry, Place, Product
from schema import PlaceSchema, ProductSchema


def clean_nan(
    data: Union[Place, Entry], keys
) -> dict:  # TODO - add this to onboarding notebook and move to post after
    data_dict = data.__dict__.copy()
    for key in keys:
        val = data_dict.get(key)
        if val is not None and isinstance(val, float) and isnan(val):
            data_dict[key] = None  # or 0.0, depending on your logic
    return data_dict


# ------------------------------ PLACES ------------------------------


async def get_all_places(db: AsyncSession) -> list[dict]:
    """Collect all places from database.

    Args:
        db (AsyncSession): db session

    Returns:
        _type_: Return tuple with all places
    """
    result = await db.execute(select(Place))
    places = result.scalars().all()
    cleaned_places = [clean_nan(p, ["lat", "lon"]) for p in places]
    return cleaned_places


# Get place by ID
async def get_place_by_id(db: AsyncSession, place_id: int) -> "Place | None":
    """Collect singe place from database.

    Args:
        db (AsyncSession):  db session
        place_id (int): id

    Returns:
        _type_: Return tuple with the place.
    """
    result = await db.execute(select(Place).where(Place.place_id == place_id))
    return result.scalars().first()


# Create or update place
async def upsert_place(db: AsyncSession, place_data: PlaceSchema):
    """Insert or Upsert new place. If place has id check if this already exisits and make an upsert if true, else create new entry. TODO: Make better checks based on further fields to avoid duplicates.

    Args:
        db (AsyncSession): db session
        place_data (PlaceSchema): tuple with place data to add or upsert
    """
    if place_data.place_id:  # update existing
        result = await db.execute(
            select(Place).where(Place.place_id == place_data.place_id)
        )
        existing_place = result.scalars().first()
        if existing_place:
            for key, value in place_data.dict(exclude_unset=True).items():
                setattr(existing_place, key, value)
            db.add(existing_place)
        else:
            # If ID provided but not found, create new
            new_place = Place(**place_data.dict(exclude={"place_id"}))
            db.add(new_place)
    else:  # create new place (no ID provided)
        new_place = Place(**place_data.dict(exclude={"place_id"}))
        db.add(new_place)

    await db.commit()


# ------------------------------ PRODUCTS ------------------------------


async def get_all_products(db: AsyncSession) -> Sequence[Product]:
    """Collect all products from database.

    Args:
        db (AsyncSession): db session

    Returns:
        _type_: Return tuple with all products
    """
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int) -> "Product | None":
    """Collect singe products from database.

    Args:
        db (AsyncSession):  db session
        product_id (int): id

    Returns:
        _type_: Return tuple with the product.
    """
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    return result.scalars().first()


async def upsert_product(db: AsyncSession, product_data: ProductSchema):
    """Insert or Upsert new product. If product has id check if this already exisits and make an upsert if true, else create new entry. TODO: Make better checks based on further fields to avoid duplicates.

    Args:
        db (AsyncSession): db session
        product_data (ProductSchema): tuple with product data to add or upsert
    """
    if product_data.product_id:  # update existing
        result = await db.execute(
            select(Product).where(Product.product_id == product_data.product_id)
        )
        existing_product = result.scalars().first()
        if existing_product:
            for key, value in product_data.dict(exclude_unset=True).items():
                setattr(existing_product, key, value)
            db.add(existing_product)
        else:
            # If ID provided but not found, create new
            new_product = Product(**product_data.dict(exclude={"product_id"}))
            db.add(new_product)
    else:  # create new product (no ID provided)
        new_product = Product(**product_data.dict(exclude={"product_id"}))
        db.add(new_product)

    await db.commit()


# ------------------------------ ENTRIES ------------------------------


async def get_all_entries(db: AsyncSession) -> list[dict]:
    result = await db.execute(select(Entry))
    entries = result.scalars().all()
    cleaned_entries = [
        clean_nan(p, ["price", "volume"]) for p in entries
    ]  # TODO remove hardcoded strings, improve preprocess
    return cleaned_entries


async def get_entry_by_id(db: AsyncSession, entry_id: int):
    result = await db.execute(select(Entry).where(Entry.entry_id == entry_id))
    return result.scalars().first()


async def create_entry(db: AsyncSession, entry_data: dict):
    entry_data = entry_data.dict()
    new_product = Entry(**entry_data)
    db.add(new_product)
    await db.commit()
