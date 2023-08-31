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

/**
 * Returns a CSS selector for an element with `data-cy="key"` attribute.
 */
const cyAttr = (key: string) => `[data-cy="${key}"]`;

/**
 * Selectors for commonly used data-cy attributes.
 */
export const CyAttr = {
  AboutMe: cyAttr("about_me"),
  ContactName: cyAttr("contact_name"),
  ContactMethod: cyAttr("contact_method"),
  ContactMessage: cyAttr("contact_message"),
  ContactSubmit: cyAttr("contact_submit"),
  ContactSuccess: cyAttr("contact_success"),
  Feed: cyAttr("feed"),
  Github: cyAttr("github"),
  Search: cyAttr("search"),
  SearchIcon: cyAttr("search_icon"),
  PageNext: cyAttr("next_page"),
  PageLast: cyAttr("last_page"),
  SiteName: cyAttr("site_name"),
};
