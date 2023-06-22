import { Api, SearchSuggestion } from "../../api";
import { changePage } from "../../page-transitions";
import React, { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { useTextEventListener } from "../../util/listeners";
import { Time } from "../datetime";
import { Scrim } from "../dialog";
import { LoadingSpinner } from "../loading";

const formID = "search_form";
const iconID = "search_icon";
const inputID = "search";
const resultsID = "search_results";

const formElement = () => document.getElementById(formID) as HTMLFormElement;
const iconElement = () => document.getElementById(iconID);
const inputElement = () => document.getElementById(inputID) as HTMLInputElement;
const resultsAppContainer = () => document.getElementById(resultsID);

const initSearch = () => {
    // Replace the default form submission so we can animate the page change
    const form = document.getElementById(formID);
    form.addEventListener("submit", ev => {
        ev.preventDefault();

        const data = new FormData(ev.target as HTMLFormElement);
        const params = new URLSearchParams(data as any);
        const searchUrl = `/search/?${params}`;
        changePage(searchUrl);
    });

    iconElement().addEventListener("focus", () => {
        // Move focus to search box when icon is selected
        const search = inputElement();
        search.focus();
    });

    formElement().addEventListener("focusin", ev => {
        iconElement().tabIndex = -1;
        Scrim.show();
    });

    formElement().addEventListener("focusout", ev => {
        // Hide scrim once focus leaves the element tree.
        if (
            !(ev.currentTarget as HTMLElement).contains(
                ev.relatedTarget as HTMLElement
            )
        ) {
            iconElement().tabIndex = 0;
            Scrim.hide();
        }
    });

    SearchApp();
};

const SearchApp = () => {
    const container = resultsAppContainer();

    if (container) {
        const root = createRoot(container);
        root.render(
            <StrictMode>
                <Search />
            </StrictMode>
        );
    }
};

const Search = () => {
    const [query, setQuery] = useState(undefined);
    const [results, setResults] = useState<SearchSuggestion[]>();

    useTextEventListener(inputID, setQuery, "keyup");

    useEffect(() => {
        if (query === undefined) {
            setQuery(inputElement().value);
            return;
        }

        Api.search(query).then(items => setResults(items.slice(0, 5)));
    }, [query]);

    return (
        <>
            <SearchResults results={results} />
            <SearchSuggestions />
        </>
    );
};

interface SearchQueryProps {
    results: SearchSuggestion[];
}
const SearchResults = (props: SearchQueryProps) => {
    const { results } = props;

    if (!results) return null;

    return (
        <>
            {results.map(item => (
                <a className="search-result" href={item.url} key={item.url}>
                    <div className="search-result--name">{item.name}</div>
                    <div className="search-result--description">
                        {item.description}
                    </div>
                    <Time dateTime={item.timestamp} />
                </a>
            ))}
        </>
    );
};

const SearchSuggestions = () => {
    const [suggestions, setSuggestions] = useState<SuggestionProps[]>();

    useEffect(() => {
        Api.searchSuggestions()
            .then(setSuggestions)
            .catch(err => {
                console.error(err);
                setSuggestions(null);
            });
    }, []);

    if (suggestions === undefined) return <LoadingSpinner />;
    if (suggestions === null) return null;

    return (
        <div className="search-suggestions">
            <div className="links-title">Explore</div>
            {suggestions.map(suggestion => (
                <Suggestion key={suggestion.url} {...suggestion} />
            ))}
        </div>
    );
};

interface SuggestionProps {
    url: string;
    name: string;
}
const Suggestion = (props: SuggestionProps) => {
    const { url, name } = props;
    return (
        <a href={url} className="search-suggestion">
            {name}
        </a>
    );
};

initSearch();
