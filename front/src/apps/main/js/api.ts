import { loadJson } from "./util/requests";

export const Api = {
    githubEvents: () =>
        loadJson("/api/github-events/").then(data => data.events),
    search: (query: string) =>
        loadJson<SearchSuggestion[]>(`/api/search/?query=${query}`).then(
            data => data.feed
        ),
    searchSuggestions: () =>
        loadJson<SearchSuggestion[]>("/api/search/suggestions/").then(
            data => data.suggestions
        ),
};

export interface SearchSuggestion {
    name: string;
    url: string;
    timestamp: string | null;
    description: string | null;
}
