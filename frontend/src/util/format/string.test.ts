import { describe } from "@jest/globals";
import { getPlaintextSummaryFromHtml } from "./string";

jest.mock("next/og", () => ({
  ImageResponse: jest.fn(() => {
    return {};
  }),
}));

describe("opengraph image generation", () => {
  test("getPlaintextSummaryFromHtml", () => {
    expect(getPlaintextSummaryFromHtml("Basic text")).toBe("Basic text");
    expect(getPlaintextSummaryFromHtml("<p>Basic text</p>")).toBe("Basic text");
    expect(getPlaintextSummaryFromHtml("<p>Basic <a>text</a></p>")).toBe(
      "Basic text",
    );
    expect(
      getPlaintextSummaryFromHtml('<p>Basic text <img src="#"/></p>'),
    ).toBe("Basic text");

    expect(
      getPlaintextSummaryFromHtml(
        '<p>Basic text <img src="#"/></p><p>Another paragraph</p>',
      ),
    ).toBe("Basic text");
    expect(
      getPlaintextSummaryFromHtml(
        '<div>Basic text <img src="#"/></div><div>Another paragraph</div>',
      ),
    ).toBe("Basic text");

    expect(
      getPlaintextSummaryFromHtml("<!-- ignore this --><p>Basic text</p>"),
    ).toBe("Basic text");
    expect(
      getPlaintextSummaryFromHtml("<p><!-- ignore this -->Basic text</p>"),
    ).toBe("Basic text");
  });
});
