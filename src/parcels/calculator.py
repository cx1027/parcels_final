from typing import List

from parcels.models import Parcel, ParcelResult, CostResult


class ParcelCostCalculator:
    """Calculates delivery costs for parcels based on their dimensions."""

    SIZE_CATEGORIES = [
        ("Small", 10.0, 3.0),
        ("Medium", 50.0, 8.0),
        ("Large", 100.0, 15.0),
        ("XL", None, 25.0),
    ]

    @classmethod
    def classify(cls, parcel: Parcel) -> str:
        """Return the size category for a parcel based on its dimensions."""
        max_dimension = max(parcel.length, parcel.width, parcel.height)

        if max_dimension >= 100.0:
            return "XL"

        if max_dimension < 10.0:
            return "Small"

        if max_dimension < 50.0:
            return "Medium"

        return "Large"

    @classmethod
    def get_cost(cls, parcel_type: str) -> float:
        """Return the fixed delivery cost for a given parcel type."""
        costs = {
            "Small": 3.0,
            "Medium": 8.0,
            "Large": 15.0,
            "XL": 25.0,
        }
        return costs[parcel_type]

    @classmethod
    def calculate(cls, parcels: List[Parcel]) -> CostResult:
        """Calculate the cost for each parcel and return individual results plus total.

        Each parcel is independently classified and charged at its cheapest rate.
        If a parcel has speedy=True, its base cost is doubled as a speedy surcharge.
        Individual parcel base costs remain unchanged.
        """
        if not parcels:
            return CostResult(parcels=[], total_cost=0.0, speedy_total_cost=0.0)

        parcel_results = []
        total = 0.0
        speedy_total = 0.0

        for parcel in parcels:
            parcel_type = cls.classify(parcel)
            cost = cls.get_cost(parcel_type)
            speedy_cost = cost if parcel.speedy else 0.0
            parcel_results.append(
                ParcelResult(
                    parcel=parcel,
                    type=parcel_type,
                    cost=cost,
                    speedy_cost=speedy_cost,
                    speedy_service=speedy_cost,
                )
            )
            total += cost + speedy_cost
            speedy_total += speedy_cost * 2

        return CostResult(
            parcels=parcel_results,
            total_cost=total,
            speedy_total_cost=speedy_total,
        )
