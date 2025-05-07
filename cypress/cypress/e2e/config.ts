const PORT: number = 80;
const SERVER: string = `nginx:${PORT}`;

/**
 * Test data includes posts that are marked as unpublished and adds
 * PrivateContentTag to their displayable content. These should never be
 * accessible to the frontend  and any test failure resulting from this means
 * the backend is leaking unpublished content.
 */
export const PrivateContentTag = "__PRIVATE__";

export const testAttr = (key: string) => `[data-testid="${key}"]`;

export const TestTarget = {
  AllowRemoteContent: testAttr("allow_remote_content"),
  RecaptchaWrapper: testAttr("recaptcha_wrapper"),
  GithubActivity: testAttr("github_activity"),
  Search: {
    Button: testAttr("search_button"),
    Input: testAttr("search_input"),
  },
  Contact: {
    Form: testAttr("contact_form"),
    Name: testAttr("contact_name"),
    Method: testAttr("contact_method"),
    Message: testAttr("contact_message"),
    Success: testAttr("contact_success"),
  },
};

export const Navigation = {
  home: () => "/",
  about: () => "/about/",
  contact: () => "/contact/",
  search: (query: string) => `/?query=${query}`,
  searchTag: (tag: string) => `/?tag=${tag}`,
  post: (slug: string) => `/posts/${slug}/`,
  app: (slug: string) => `/apps/${slug}/`,
  changelog: (slug: string) => `/changelog/${slug}/`,
};

/**
 * List of urls which are representative of all possible content.
 */
export const RepresentativeUrls = [
  Navigation.home(),
  Navigation.about(),
  Navigation.contact(),
  Navigation.post("test-article"),
  Navigation.app("test-app"),
  Navigation.changelog("test-changelog"),
];

export const toFilename = (url: string): string =>
  url.replace(SERVER, "").replace(/\//g, "--").replace(/[?=.]/g, "_");
