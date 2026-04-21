from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Parcel:
    """Represents a parcel with its physical dimensions.

    All dimensions are in centimeters.
    """
    length: float
    width: float
    height: float


@dataclass(frozen=True)
class ParcelResult:
    """The cost calculation result for a single parcel."""
    parcel: Parcel
    type: str
    cost: float


@dataclass(frozen=True)
class SpeedyResult:
    """The cost breakdown for speedy shipping."""
    base_cost: float
    speedy_cost: float
    total_cost: float


@dataclass(frozen=True)
class CostResult:
    """The overall cost calculation result for a collection of parcels."""
    parcels: List[ParcelResult]
    total_cost: float
    speedy_cost: float = 0.0
    speedy_service: SpeedyResult = None
