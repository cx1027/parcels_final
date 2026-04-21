# Parcels Library

A Python library for calculating parcel delivery costs based on dimensions.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from parcels import Parcel, ParcelCostCalculator

# Create a parcel with dimensions (length, width, height in cm)
parcel = Parcel(length=15, width=10, height=5)
result = ParcelCostCalculator.calculate([parcel])

for item in result.parcels:
    print(f"Type: {item.type}, Cost: ${item.cost}")

print(f"Total: ${result.total_cost}")
```

## Parcel Size Categories

| Size   | Dimensions           | Cost |
|--------|----------------------|------|
| Small  | All dimensions < 10cm| $3   |
| Medium | All dimensions < 50cm| $8   |
| Large  | All dimensions < 100cm| $15  |
| XL     | Any dimension >= 100cm| $25  |
