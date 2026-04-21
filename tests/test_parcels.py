import pytest
from parcels import Parcel, ParcelCostCalculator, CostResult, ParcelResult, SpeedyResult


class TestParcelClassification:
    """Tests for parcel size classification."""

    def test_small_parcel_all_dimensions_under_10cm(self):
        parcel = Parcel(length=5, width=5, height=5)
        assert ParcelCostCalculator.classify(parcel) == "Small"

    def test_small_parcel_with_nearly_zero_dimensions(self):
        parcel = Parcel(length=0.1, width=0.1, height=0.1)
        assert ParcelCostCalculator.classify(parcel) == "Small"

    def test_medium_parcel_all_dimensions_under_50cm(self):
        parcel = Parcel(length=30, width=40, height=45)
        assert ParcelCostCalculator.classify(parcel) == "Medium"

    def test_medium_parcel_at_boundary_10cm_exactly(self):
        parcel = Parcel(length=10, width=5, height=5)
        assert ParcelCostCalculator.classify(parcel) == "Medium"

    def test_large_parcel_all_dimensions_under_100cm(self):
        parcel = Parcel(length=60, width=70, height=80)
        assert ParcelCostCalculator.classify(parcel) == "Large"

    def test_large_parcel_at_boundary_50cm_exactly(self):
        parcel = Parcel(length=50, width=30, height=20)
        assert ParcelCostCalculator.classify(parcel) == "Large"

    def test_xl_parcel_one_dimension_at_100cm(self):
        parcel = Parcel(length=100, width=30, height=20)
        assert ParcelCostCalculator.classify(parcel) == "XL"

    def test_xl_parcel_any_dimension_over_100cm(self):
        parcel = Parcel(length=150, width=20, height=20)
        assert ParcelCostCalculator.classify(parcel) == "XL"

    def test_xl_parcel_width_over_100cm(self):
        parcel = Parcel(length=20, width=150, height=20)
        assert ParcelCostCalculator.classify(parcel) == "XL"

    def test_xl_parcel_height_over_100cm(self):
        parcel = Parcel(length=20, width=20, height=150)
        assert ParcelCostCalculator.classify(parcel) == "XL"


class TestParcelCosts:
    """Tests for individual parcel cost retrieval."""

    def test_small_cost(self):
        assert ParcelCostCalculator.get_cost("Small") == 3.0

    def test_medium_cost(self):
        assert ParcelCostCalculator.get_cost("Medium") == 8.0

    def test_large_cost(self):
        assert ParcelCostCalculator.get_cost("Large") == 15.0

    def test_xl_cost(self):
        assert ParcelCostCalculator.get_cost("XL") == 25.0


class TestCostCalculation:
    """Tests for the full cost calculation pipeline."""

    def test_single_small_parcel(self):
        parcel = Parcel(length=5, width=5, height=5)
        result = ParcelCostCalculator.calculate([parcel])

        assert result.total_cost == 3.0
        assert len(result.parcels) == 1
        assert result.parcels[0].type == "Small"
        assert result.parcels[0].cost == 3.0
        assert result.parcels[0].parcel == parcel

    def test_single_medium_parcel(self):
        parcel = Parcel(length=30, width=20, height=15)
        result = ParcelCostCalculator.calculate([parcel])

        assert result.total_cost == 8.0
        assert result.parcels[0].type == "Medium"
        assert result.parcels[0].cost == 8.0

    def test_single_large_parcel(self):
        parcel = Parcel(length=80, width=60, height=70)
        result = ParcelCostCalculator.calculate([parcel])

        assert result.total_cost == 15.0
        assert result.parcels[0].type == "Large"
        assert result.parcels[0].cost == 15.0

    def test_single_xl_parcel(self):
        parcel = Parcel(length=120, width=50, height=50)
        result = ParcelCostCalculator.calculate([parcel])

        assert result.total_cost == 25.0
        assert result.parcels[0].type == "XL"
        assert result.parcels[0].cost == 25.0

    def test_multiple_parcels_mixed_sizes(self):
        parcels = [
            Parcel(length=5, width=5, height=5),
            Parcel(length=30, width=20, height=15),
            Parcel(length=80, width=60, height=70),
            Parcel(length=120, width=50, height=50),
        ]
        result = ParcelCostCalculator.calculate(parcels)

        assert len(result.parcels) == 4
        assert result.parcels[0].type == "Small"
        assert result.parcels[1].type == "Medium"
        assert result.parcels[2].type == "Large"
        assert result.parcels[3].type == "XL"
        assert result.total_cost == 3.0 + 8.0 + 15.0 + 25.0

    def test_empty_list_returns_zero_total(self):
        result = ParcelCostCalculator.calculate([])

        assert result.total_cost == 0.0
        assert result.parcels == []

    def test_result_is_cost_result_instance(self):
        parcel = Parcel(length=5, width=5, height=5)
        result = ParcelCostCalculator.calculate([parcel])

        assert isinstance(result, CostResult)

    def test_each_parcel_result_is_parcel_result_instance(self):
        parcels = [
            Parcel(length=5, width=5, height=5),
            Parcel(length=30, width=20, height=15),
        ]
        result = ParcelCostCalculator.calculate(parcels)

        for item in result.parcels:
            assert isinstance(item, ParcelResult)


class TestSpeedyShipping:
    """Tests for speedy shipping cost calculation."""

    def test_speedy_doubles_total_cost(self):
        parcel = Parcel(length=5, width=5, height=5)
        result = ParcelCostCalculator.calculate_with_speedy([parcel])

        assert result.total_cost == 6.0

    def test_speedy_cost_equals_base_cost(self):
        parcel = Parcel(length=5, width=5, height=5)
        result = ParcelCostCalculator.calculate_with_speedy([parcel])

        assert result.speedy_cost == 3.0

    def test_speedy_service_is_separate_item(self):
        parcel = Parcel(length=5, width=5, height=5)
        result = ParcelCostCalculator.calculate_with_speedy([parcel])

        assert result.speedy_service is not None
        assert isinstance(result.speedy_service, SpeedyResult)
        assert result.speedy_service.base_cost == 3.0
        assert result.speedy_service.speedy_cost == 3.0
        assert result.speedy_service.total_cost == 6.0

    def test_individual_parcel_costs_unchanged(self):
        parcels = [
            Parcel(length=5, width=5, height=5),
            Parcel(length=30, width=20, height=15),
            Parcel(length=80, width=60, height=70),
        ]
        base_result = ParcelCostCalculator.calculate(parcels)
        speedy_result = ParcelCostCalculator.calculate_with_speedy(parcels)

        assert base_result.parcels[0].cost == speedy_result.parcels[0].cost
        assert base_result.parcels[1].cost == speedy_result.parcels[1].cost
        assert base_result.parcels[2].cost == speedy_result.parcels[2].cost

    def test_speedy_multiple_parcels(self):
        parcels = [
            Parcel(length=5, width=5, height=5),
            Parcel(length=30, width=20, height=15),
        ]
        result = ParcelCostCalculator.calculate_with_speedy(parcels)

        assert result.total_cost == (3.0 + 8.0) * 2
        assert result.speedy_cost == 3.0 + 8.0

    def test_speedy_empty_list(self):
        result = ParcelCostCalculator.calculate_with_speedy([])

        assert result.total_cost == 0.0
        assert result.speedy_cost == 0.0
        assert result.speedy_service.base_cost == 0.0
        assert result.speedy_service.speedy_cost == 0.0
        assert result.speedy_service.total_cost == 0.0
