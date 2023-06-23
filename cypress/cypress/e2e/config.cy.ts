const PORT: number = 8123;
const SERVER: string = `localhost:${PORT}`;

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
