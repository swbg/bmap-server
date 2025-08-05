from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    String,
    MetaData,
    UniqueConstraint,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship

# Point to public schema explicitly
metadata = MetaData(schema="public")
Base = declarative_base(metadata=metadata)


class Place(Base):
    __tablename__ = "places"

    placeId = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    placeName = Column(String(255), nullable=False)
    placeType = Column(String(255))
    address = Column(String(255))
    website = Column(String(255))
    phone = Column(String(50))
    note = Column(String(255))
    validUntil = Column(Date)


class Product(Base):
    __tablename__ = "products"

    productId = Column(Integer, primary_key=True, index=True)
    brandName = Column(String(255))
    productName = Column(String(255))
    productType = Column(String(255))


class Entry(Base):
    __tablename__ = "entries"
    __table_args__ = (
        UniqueConstraint(
            "placeId", "productId", "validFrom", name="unique_place_product_validfrom"
        ),
    )

    entryId = Column(Integer, primary_key=True, index=True)
    placeId = Column(
        Integer,
        ForeignKey("places.placeId", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    productId = Column(
        Integer,
        ForeignKey("products.productId", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    price = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    vomFass = Column(Boolean, nullable=True)
    validFrom = Column(Date, nullable=True)
    lastUpdate = Column(Date, nullable=True)
    validUntil = Column(Date, nullable=True)

    # Optional relationships (if you want to access places/products easily)
    place = relationship("Place")
    product = relationship("Product")
