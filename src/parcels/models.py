from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Parcel:
    """Represents a parcel with its physical dimensions.

    All dimensions are in centimeters.
    speedy indicates whether speedy shipping is requested for this parcel.
    """
    length: float
    width: float
    height: float
    speedy: bool = False


@dataclass(frozen=True)
class ParcelResult:
    """The cost calculation result for a single parcel."""
    parcel: Parcel
    type: str
    cost: float
    speedy_cost: float = 0.0
    speedy_service: float = None


@dataclass(frozen=True)
class CostResult:
    """The overall cost calculation result for a collection of parcels."""
    parcels: List[ParcelResult]
    total_cost: float
    speedy_total_cost: float = 0.0
