"""Pricing service for calculating parcel delivery costs."""
from parcels.models import Parcel, ParcelType, PricingResult, OrderPricingResult


# Fixed costs per parcel type
PARCEL_COSTS: dict[ParcelType, float] = {
    ParcelType.SMALL: 3.0,
    ParcelType.MEDIUM: 8.0,
    ParcelType.LARGE: 15.0,
    ParcelType.XL: 25.0,
}


def _classify_by_size(parcel: Parcel) -> ParcelType:
    """Classify a parcel by its dimensions into a size category.

    Classification rules:
    - XL: any dimension >= 100cm
    - Large: all dimensions < 100cm
    - Medium: all dimensions < 50cm
    - Small: all dimensions < 10cm
    """
    max_dim = max(parcel.length, parcel.width, parcel.height)

    if max_dim >= 100:
        return ParcelType.XL
    if max(parcel.length, parcel.width, parcel.height) < 100:
        if parcel.length < 50 and parcel.width < 50 and parcel.height < 50:
            if parcel.length < 10 and parcel.width < 10 and parcel.height < 10:
                return ParcelType.SMALL
            return ParcelType.MEDIUM
        return ParcelType.LARGE

    return ParcelType.LARGE


def price_parcel(parcel: Parcel) -> PricingResult:
    """Calculate the delivery cost for a single parcel.

    Returns a PricingResult containing the parcel, its type, and cost.
    """
    parcel_type = _classify_by_size(parcel)
    cost = PARCEL_COSTS[parcel_type]
    return PricingResult(parcel=parcel, parcel_type=parcel_type, cost=cost)


def price_order(parcels: list[Parcel]) -> OrderPricingResult:
    """Calculate the total cost for an order of parcels.

    Each parcel is priced individually and the cheapest option is selected
    (which is the default size-based pricing in this implementation).

    Returns an OrderPricingResult containing individual item breakdowns
    and the total cost.
    """
    if not parcels:
        return OrderPricingResult(items=(), total_cost=0.0)

    priced_items = tuple(price_parcel(p) for p in parcels)
    total = sum(item.cost for item in priced_items)

    return OrderPricingResult(items=priced_items, total_cost=total)
