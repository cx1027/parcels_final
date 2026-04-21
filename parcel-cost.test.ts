import { describe, it, expect } from "vitest";
import {
  classifyParcelSize,
  priceParcel,
  calculateParcelCosts,
} from "./src/parcel-cost.service";
import { Parcel, ParcelSize } from "./src/parcel.model";

describe("classifyParcelSize", () => {
  it("classifies as Small when all dimensions < 10cm", () => {
    expect(classifyParcelSize({ lengthCm: 5, widthCm: 5, heightCm: 5 })).toBe("Small");
    expect(classifyParcelSize({ lengthCm: 9, widthCm: 9, heightCm: 9 })).toBe("Small");
    expect(classifyParcelSize({ lengthCm: 1, widthCm: 1, heightCm: 9 })).toBe("Small");
  });

  it("classifies as Medium when max dimension < 50cm and not Small", () => {
    expect(classifyParcelSize({ lengthCm: 30, widthCm: 20, heightCm: 15 })).toBe("Medium");
    expect(classifyParcelSize({ lengthCm: 49, widthCm: 1, heightCm: 1 })).toBe("Medium");
  });

  it("classifies as Large when max dimension < 100cm and not Small or Medium", () => {
    expect(classifyParcelSize({ lengthCm: 60, widthCm: 70, heightCm: 80 })).toBe("Large");
    expect(classifyParcelSize({ lengthCm: 99, widthCm: 1, heightCm: 1 })).toBe("Large");
  });

  it("classifies as XL when any dimension >= 100cm", () => {
    expect(classifyParcelSize({ lengthCm: 100, widthCm: 1, heightCm: 1 })).toBe("XL");
    expect(classifyParcelSize({ lengthCm: 150, widthCm: 200, heightCm: 50 })).toBe("XL");
    expect(classifyParcelSize({ lengthCm: 5, widthCm: 5, heightCm: 100 })).toBe("XL");
  });
});

describe("priceParcel", () => {
  const cases: Array<{ parcel: Parcel; expectedSize: ParcelSize; expectedCost: number }> = [
    { parcel: { lengthCm: 5, widthCm: 5, heightCm: 5 }, expectedSize: "Small", expectedCost: 3 },
    { parcel: { lengthCm: 30, widthCm: 20, heightCm: 15 }, expectedSize: "Medium", expectedCost: 8 },
    { parcel: { lengthCm: 60, widthCm: 70, heightCm: 80 }, expectedSize: "Large", expectedCost: 15 },
    { parcel: { lengthCm: 100, widthCm: 50, heightCm: 50 }, expectedSize: "XL", expectedCost: 25 },
  ];

  cases.forEach(({ parcel, expectedSize, expectedCost }) => {
    it(`prices ${expectedSize} parcel at $${expectedCost}`, () => {
      const result = priceParcel(parcel);
      expect(result.size).toBe(expectedSize);
      expect(result.cost).toBe(expectedCost);
      expect(result.lengthCm).toBe(parcel.lengthCm);
      expect(result.widthCm).toBe(parcel.widthCm);
      expect(result.heightCm).toBe(parcel.heightCm);
    });
  });
});

describe("calculateParcelCosts", () => {
  it("returns empty result for no parcels", () => {
    const result = calculateParcelCosts([]);
    expect(result.parcels).toHaveLength(0);
    expect(result.totalCost).toBe(0);
  });

  it("calculates correct total for mixed parcels", () => {
    const parcels = [
      { lengthCm: 5, widthCm: 5, heightCm: 5 },
      { lengthCm: 30, widthCm: 20, heightCm: 15 },
      { lengthCm: 60, widthCm: 70, heightCm: 80 },
    ];
    const result = calculateParcelCosts(parcels);
    expect(result.parcels).toHaveLength(3);
    expect(result.totalCost).toBe(3 + 8 + 15);
  });

  it("selects cheapest option per parcel", () => {
    const parcels = [
      { lengthCm: 5, widthCm: 5, heightCm: 5 },
      { lengthCm: 100, widthCm: 100, heightCm: 100 },
    ];
    const result = calculateParcelCosts(parcels);
    expect(result.parcels[0].size).toBe("Small");
    expect(result.parcels[0].cost).toBe(3);
    expect(result.parcels[1].size).toBe("XL");
    expect(result.parcels[1].cost).toBe(25);
    expect(result.totalCost).toBe(28);
  });
});
