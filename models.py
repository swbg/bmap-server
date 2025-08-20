from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, relationship

# Point to public schema explicitly
metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class Place(Base):
    __tablename__ = "places"

    place_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    place_name = Column(String(255), nullable=False)
    place_type = Column(String(255))
    address = Column(String(255))
    website = Column(String(255))
    phone = Column(String(50))
    note = Column(String(255))
    valid_until = Column(Date, nullable=True)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_name = Column(String(255))
    product_name = Column(String(255))
    product_type = Column(String(255))


class Entry(Base):
    __tablename__ = "entries"
    __table_args__ = (
        UniqueConstraint(
            "place_id",
            "product_id",
            "valid_from",
            name="unique_place_product_validfrom",
        ),
    )

    entry_id = Column(Integer, primary_key=True, index=True)
    place_id = Column(
        Integer,
        ForeignKey("places.place_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    price = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    vom_fass = Column(Boolean, nullable=True)
    valid_from = Column(Date, nullable=True)
    last_update = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)

    # Optional relationships (if you want to access places/products easily)
    place = relationship("Place")
    product = relationship("Product")
