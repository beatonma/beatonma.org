import { describe } from "@jest/globals";
import { formatMediaDuration } from "@/util/format/duration";

describe("duration formatting", () => {
  test("formatMediaDuration is correct", () => {
    expect(formatMediaDuration(0)).toBe("0:00");
    expect(formatMediaDuration(1)).toBe("0:01");
    expect(formatMediaDuration(10)).toBe("0:10");
    expect(formatMediaDuration(59)).toBe("0:59");
    expect(formatMediaDuration(60)).toBe("1:00");
    expect(formatMediaDuration(61)).toBe("1:01");
    expect(formatMediaDuration(3599)).toBe("59:59");
    expect(formatMediaDuration(3601)).toBe("1:00:01");
    expect(formatMediaDuration(3661)).toBe("1:01:01");
  });
});
