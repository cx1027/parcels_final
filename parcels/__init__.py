"""Parcels pricing library.

A library for calculating the cost of sending parcels based on size categories.

Usage:
    from parcels import Parcel, price_parcel, price_order

    parcel = Parcel(length=5, width=5, height=5)
    result = price_parcel(parcel)

    order = [Parcel(5, 5, 5), Parcel(30, 30, 30)]
    order_result = price_order(order)
"""

from parcels.models import (
    Parcel,
    ParcelType,
    PricingResult,
    OrderPricingResult,
)
from parcels.pricing import price_parcel, price_order

__all__ = [
    "Parcel",
    "ParcelType",
    "PricingResult",
    "OrderPricingResult",
    "price_parcel",
    "price_order",
]
