import { Event } from "../apps/github-events//types";
import { loadJson } from "./../util/requests";

export const Api = {
    githubEvents: () => loadJson<GithubEventsResponse>("/api/github/events/"),
    search: (query: string) =>
        loadJson<SearchResponse>(`/api/search/?query=${query}`).then(
            data => data.feed,
        ),
    searchSuggestions: () =>
        loadJson<SuggestionResponse>("/api/search/suggestions/"),
};

export interface SearchSuggestion {
    name: string;
    url: string;
    timestamp: string | null;
    description: string | null;
    className: string | null;
}

interface SearchResponse {
    query: string;
    feed: SearchSuggestion[];
}

type SuggestionResponse = SearchSuggestion[];

type GithubEventsResponse = Event[];
