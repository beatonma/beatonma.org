const PORT: number = 8123;
const SERVER: string = `localhost:${PORT}`;

/**
 * Test data includes posts that are marked as unpublished and adds
 * PrivateContentTag to their displayable content. These should never be
 * accessible to the frontend  and any test failure resulting from this means
 * the backend is leaking unpublished content.
 */
export const PrivateContentTag = "__PRIVATE__";

/**
 * List of urls which are representative of all possible content.
 */
export const RepresentativeUrls = [
  "/",
  "/?page=2",
  "/about/",
  "/contact/",
  "/search/?query=target",
  "/tag/sample-tag/",
  "/language/TestTarget-Language/",
  "/app/testtarget.app/",
  "/a/230203-testtarget-article/",
  "/blog/230203-testtarget-blog/",
];

export const toFilename = (url: string): string =>
  url.replace(SERVER, "").replace(/\//g, "--").replace(/[?=.]/g, "_");
