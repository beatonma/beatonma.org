import { formatUrl } from "@/util/transforms";

describe("transforms", () => {
  test("formatUrl", () => {
    [
      ["https://github.com/beatonma/", "github/@beatonma"],
      ["https://github.com/beatonma/beatonma.org", "github/beatonma.org"],
      [
        "https://github.com/beatonma/beatonma.org/blob/main/README.md",
        "github/beatonma.org",
      ],
      ["https://www.youtube.com/watch?v=AvlonenyDh4", "youtube.com"],
      ["https://www.youtube.com/@fallofmath", "youtube/fallofmath"],
      ["https://reddit.com/u/username", "u/username"],
      ["https://reddit.com/r/subreddit", "r/subreddit"],
      ["https://pypi.org/project/django-wm/", "pypi/django-wm"],
      ["https://pypi.org/user/beatonma/", "pypi/beatonma"],
    ].forEach(([url, expected]) => expect(formatUrl(url)).toBe(expected));
  });
});
