"""Data models for the parcels pricing library."""
from dataclasses import dataclass
from enum import Enum


class ParcelType(Enum):
    """Parcel size categories based on dimensions."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    XL = "xl"


@dataclass(frozen=True)
class Parcel:
    """Represents a parcel with its dimensions.

    All dimensions are in centimeters.
    """
    length: float
    width: float
    height: float
    weight: float = 0.0

    def __post_init__(self):
        if self.length <= 0 or self.width <= 0 or self.height <= 0:
            raise ValueError("All dimensions must be positive values.")
        if self.weight < 0:
            raise ValueError("Weight cannot be negative.")


@dataclass(frozen=True)
class PricingResult:
    """Result of pricing a single parcel."""
    parcel: Parcel
    parcel_type: ParcelType
    cost: float


@dataclass(frozen=True)
class OrderPricingResult:
    """Result of pricing an entire order of parcels."""
    items: tuple[PricingResult, ...]
    total_cost: float

    @property
    def breakdown(self) -> dict[ParcelType, tuple[PricingResult, ...]]:
        """Group pricing results by parcel type."""
        grouped: dict[ParcelType, list[PricingResult]] = {pt: [] for pt in ParcelType}
        for item in self.items:
            grouped[item.parcel_type].append(item)
        return {pt: tuple(items) for pt, items in grouped.items()}
