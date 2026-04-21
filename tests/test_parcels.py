"""Tests for the parcels pricing library."""
import pytest
from parcels import Parcel, ParcelType, price_parcel, price_order


class TestParcelModel:
    """Tests for the Parcel data model."""

    def test_valid_parcel(self):
        parcel = Parcel(length=10, width=20, height=30)
        assert parcel.length == 10
        assert parcel.width == 20
        assert parcel.height == 30
        assert parcel.weight == 0.0

    def test_parcel_with_weight(self):
        parcel = Parcel(length=10, width=20, height=30, weight=5.0)
        assert parcel.weight == 5.0

    def test_invalid_negative_dimension(self):
        with pytest.raises(ValueError, match="All dimensions must be positive"):
            Parcel(length=-1, width=10, height=10)

    def test_invalid_zero_dimension(self):
        with pytest.raises(ValueError, match="All dimensions must be positive"):
            Parcel(length=0, width=10, height=10)

    def test_invalid_negative_weight(self):
        with pytest.raises(ValueError, match="Weight cannot be negative"):
            Parcel(length=10, width=10, height=10, weight=-1)

    def test_parcel_is_hashable(self):
        parcel1 = Parcel(10, 20, 30)
        parcel2 = Parcel(10, 20, 30)
        assert hash(parcel1) == hash(parcel2)
        assert parcel1 == parcel2


class TestParcelClassification:
    """Tests for parcel size classification."""

    def test_small_parcel_all_under_10cm(self):
        """All dimensions < 10cm should be classified as Small ($3)."""
        parcel = Parcel(length=9, width=9, height=9)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.SMALL
        assert result.cost == 3.0

    def test_small_parcel_edge_case_just_under_10(self):
        parcel = Parcel(length=9.99, width=9.99, height=9.99)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.SMALL
        assert result.cost == 3.0

    def test_small_parcel_boundary_at_10_excluded(self):
        """Dimension exactly 10cm should NOT be small."""
        parcel = Parcel(length=10, width=9, height=9)
        result = price_parcel(parcel)
        assert result.parcel_type != ParcelType.SMALL

    def test_medium_parcel_all_under_50cm(self):
        """All dimensions < 50cm should be classified as Medium ($8)."""
        parcel = Parcel(length=49, width=49, height=49)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.MEDIUM
        assert result.cost == 8.0

    def test_medium_parcel_edge_case(self):
        parcel = Parcel(length=49.99, width=30, height=30)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.MEDIUM
        assert result.cost == 8.0

    def test_medium_parcel_one_dimension_10_or_above(self):
        """If one dimension is >= 10 but all < 50, it's still Medium."""
        parcel = Parcel(length=10, width=30, height=30)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.MEDIUM
        assert result.cost == 8.0

    def test_large_parcel_all_under_100cm(self):
        """All dimensions < 100cm (and at least one >= 50) should be Large ($15)."""
        parcel = Parcel(length=99, width=99, height=99)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.LARGE
        assert result.cost == 15.0

    def test_large_parcel_edge_case(self):
        parcel = Parcel(length=99.99, width=50, height=50)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.LARGE
        assert result.cost == 15.0

    def test_xl_parcel_any_dimension_100_or_above(self):
        """Any dimension >= 100cm should be classified as XL ($25)."""
        parcel = Parcel(length=100, width=50, height=50)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.XL
        assert result.cost == 25.0

    def test_xl_parcel_multiple_dimensions_at_100(self):
        parcel = Parcel(length=100, width=100, height=100)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.XL
        assert result.cost == 25.0

    def test_xl_parcel_large_values(self):
        parcel = Parcel(length=200, width=150, height=100)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.XL
        assert result.cost == 25.0

    def test_medium_overrides_small_when_at_least_one_dim_10_or_above(self):
        """Mixed dimensions: one at 10+, rest under 10 should be Medium."""
        parcel = Parcel(length=10, width=5, height=5)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.MEDIUM

    def test_large_overrides_medium_when_at_least_one_dim_50_or_above(self):
        """Mixed dimensions: one at 50+, rest under 50 should be Large."""
        parcel = Parcel(length=50, width=30, height=30)
        result = price_parcel(parcel)
        assert result.parcel_type == ParcelType.LARGE


class TestOrderPricing:
    """Tests for order-level pricing."""

    def test_single_parcel_order(self):
        parcel = Parcel(length=5, width=5, height=5)
        result = price_order([parcel])
        assert len(result.items) == 1
        assert result.total_cost == 3.0

    def test_multiple_parcels_order(self):
        parcels = [
            Parcel(length=5, width=5, height=5),     # Small $3
            Parcel(length=30, width=30, height=30),  # Medium $8
            Parcel(length=60, width=60, height=60),  # Large $15
        ]
        result = price_order(parcels)
        assert len(result.items) == 3
        assert result.total_cost == 26.0
        assert result.items[0].cost == 3.0
        assert result.items[1].cost == 8.0
        assert result.items[2].cost == 15.0

    def test_empty_order(self):
        result = price_order([])
        assert len(result.items) == 0
        assert result.total_cost == 0.0

    def test_all_xl_parcels(self):
        parcels = [
            Parcel(length=100, width=100, height=100),
            Parcel(length=150, width=50, height=50),
        ]
        result = price_order(parcels)
        assert result.total_cost == 50.0

    def test_breakdown_by_type(self):
        parcels = [
            Parcel(5, 5, 5),    # Small
            Parcel(5, 5, 5),    # Small
            Parcel(30, 30, 30), # Medium
        ]
        result = price_order(parcels)
        breakdown = result.breakdown
        assert len(breakdown[ParcelType.SMALL]) == 2
        assert len(breakdown[ParcelType.MEDIUM]) == 1
        assert len(breakdown[ParcelType.LARGE]) == 0
        assert len(breakdown[ParcelType.XL]) == 0

    def test_order_preserves_parcel_type_in_results(self):
        parcels = [Parcel(40, 40, 40)]
        result = price_order(parcels)
        assert result.items[0].parcel_type == ParcelType.MEDIUM
