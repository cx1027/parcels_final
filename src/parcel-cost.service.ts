import { Parcel, PricedParcel, CostingResult, ParcelSize } from "./parcel.model";

const SIZE_THRESHOLDS: Record<Exclude<ParcelSize, "XL">, number> = {
  Small: 10,
  Medium: 50,
  Large: 100,
};

const SIZE_COSTS: Record<ParcelSize, number> = {
  Small: 3,
  Medium: 8,
  Large: 15,
  XL: 25,
};

export function classifyParcelSize(parcel: Parcel): ParcelSize {
  const maxDimension = Math.max(parcel.lengthCm, parcel.widthCm, parcel.heightCm);
  if (maxDimension >= 100) return "XL";
  if (maxDimension >= 50) return "Large";
  if (maxDimension >= 10) return "Medium";
  return "Small";
}

export function priceParcel(parcel: Parcel): PricedParcel {
  const size = classifyParcelSize(parcel);
  return { ...parcel, size, cost: SIZE_COSTS[size] };
}

export function calculateParcelCosts(parcels: Parcel[]): CostingResult {
  const pricedParcels = parcels.map(priceParcel);
  const totalCost = pricedParcels.reduce((sum, p) => sum + p.cost, 0);
  return { parcels: pricedParcels, totalCost };
}
