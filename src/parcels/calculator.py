from typing import List

from parcels.models import Parcel, ParcelResult, CostResult, SpeedyResult


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
        """
        if not parcels:
            return CostResult(parcels=[], total_cost=0.0)

        parcel_results = []
        total = 0.0

        for parcel in parcels:
            parcel_type = cls.classify(parcel)
            cost = cls.get_cost(parcel_type)
            parcel_results.append(ParcelResult(parcel=parcel, type=parcel_type, cost=cost))
            total += cost

        return CostResult(parcels=parcel_results, total_cost=total)

    @classmethod
    def calculate_with_speedy(cls, parcels: List[Parcel]) -> CostResult:
        """Calculate costs with speedy shipping applied.

        Speedy shipping doubles the base cost of the order.
        The speedy surcharge is listed as a separate item and does not
        affect individual parcel costs.
        """
        if not parcels:
            base_result = CostResult(parcels=[], total_cost=0.0)
            speedy_result = SpeedyResult(base_cost=0.0, speedy_cost=0.0, total_cost=0.0)
            return CostResult(
                parcels=[], total_cost=0.0, speedy_cost=0.0, speedy_service=speedy_result
            )

        base_result = cls.calculate(parcels)
        speedy_cost = base_result.total_cost
        speedy_result = SpeedyResult(
            base_cost=base_result.total_cost,
            speedy_cost=speedy_cost,
            total_cost=base_result.total_cost + speedy_cost,
        )
        return CostResult(
            parcels=base_result.parcels,
            total_cost=speedy_result.total_cost,
            speedy_cost=speedy_cost,
            speedy_service=speedy_result,
        )
