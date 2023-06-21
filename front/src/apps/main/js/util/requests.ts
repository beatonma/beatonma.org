export const get = (url: string): Promise<Response> =>
    fetch(url, {
        method: "GET",
        credentials: "same-origin",
    });

export const loadPage = (url: string): Promise<string> =>
    get(url).then(response => response.text());

export const loadJson = <T>(url: string): Promise<any> =>
    get(url).then(response => response.json());
