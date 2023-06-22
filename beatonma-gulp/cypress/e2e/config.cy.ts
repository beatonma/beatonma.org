const PORT: number = 8123;
const SERVER: string = `localhost:${PORT}`;

export const serverUrl = (path: string) =>
    `${SERVER}/${path}`.replace("//", "/");

/**
 * List of urls which are representative of all possible content.
 */
export const RepresentativeUrls = [
    serverUrl("/"),
    serverUrl("/?page=2"),
    serverUrl("/about/"),
    serverUrl("/contact/"),
    serverUrl("/search/?query=target"),
    serverUrl("/tag/sample-tag/"),
    serverUrl("/language/TestTarget-Language/"),
    serverUrl("/app/testtarget.app/"),
    serverUrl("/a/230203-testtarget-article/"),
    serverUrl("/blog/230203-testtarget-blog/"),
];

export const toFilename = (url: string): string =>
    url.replace(SERVER, "").replace(/\//g, "--").replace(/[?=.]/g, "_");
