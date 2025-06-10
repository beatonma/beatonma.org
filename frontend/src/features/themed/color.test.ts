import { describe, test } from "@jest/globals";
import expect from "expect";
import { _private } from "@/features/themed/color";

describe("Color tests", () => {
  test("resolveToRgb rgb", () => {
    expect(_private.resolveToRgb("rgb(255, 0, 0)")).toEqual([255, 0, 0]);
    expect(_private.resolveToRgb("rgb(0  255 0)")).toEqual([0, 255, 0]);
    expect(_private.resolveToRgb("rgb(0, 0, 255)")).toEqual([0, 0, 255]);
  });

  test("resolveToRgb rgb numbers only", () => {
    expect(_private.resolveToRgb("255, 0, 0")).toEqual([255, 0, 0]);
    expect(_private.resolveToRgb("0  255 0")).toEqual([0, 255, 0]);
    expect(_private.resolveToRgb("0, 0, 255")).toEqual([0, 0, 255]);
  });

  test("resolveToRgb rgb with alpha", () => {
    expect(_private.resolveToRgb("rgb(0 0 255 / 50)")).toEqual([0, 0, 255]);
    expect(_private.resolveToRgb("rgba(0, 0, 255, .5)")).toEqual([0, 0, 255]);
  });

  test("resolveToRgb hex codes", () => {
    expect(_private.resolveToRgb("#ff0000")).toEqual([255, 0, 0]);
    expect(_private.resolveToRgb("00ff00")).toEqual([0, 255, 0]);
    expect(_private.resolveToRgb("0000ff")).toEqual([0, 0, 255]);
  });
});
