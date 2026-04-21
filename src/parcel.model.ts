export type ParcelSize = "Small" | "Medium" | "Large" | "XL";

export interface Parcel {
  readonly lengthCm: number;
  readonly widthCm: number;
  readonly heightCm: number;
}

export interface PricedParcel extends Parcel {
  readonly size: ParcelSize;
  readonly cost: number;
}

export interface CostingResult {
  readonly parcels: readonly PricedParcel[];
  readonly totalCost: number;
}
