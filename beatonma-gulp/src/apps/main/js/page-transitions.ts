/**
 * Expected structure:
 *
 *   <div id="{contentWrapperID}>
 *     <div id="{contentID}">
 *       <!-- Animated content here -->
 *     </div>
 *   </div>
 */
import { APPS } from "./apps";
import { Scaffold } from "./dom";
import { loadPage } from "./util/requests";

const ItemAnimationDelay = 40;
const PageAnimationDuration = 200;

// Links with this class opt out of hot-swapping content.
const NoAnimationClass = "noanim";

// Disable animations when the URL path matches this pattern.
const NoAnimationPathsRegex = /(webapp)\/.*/;

const OnPageChangeClass = ".onPageChange";
const OnPageUnloadClass = ".onPageUnload";

const AnimatedElementSelector = ".h-entry, .card";

export const animatedItemProps = (index: number) => {
    return {
        "data-animate-in": true,
        style: {
            animationDelay: `${ItemAnimationDelay * index}ms`,
        },
    };
};

const onContentChanged = async (dom: Document | HTMLElement) => {
    APPS.forEach(app => {
        try {
            app(dom);
        } catch (e) {
            console.error(`App ${app.name} failed: ${e}`);
        }
    });

    if (window.location.hash) {
        scrollToId(window.location.hash);
    }
};

const getScript = async (element: HTMLScriptElement) => {
    const src = element.src;
    element.parentElement.removeChild(element);

    const script: HTMLScriptElement = document.createElement("script");
    script.async = true;
    script.src = src;

    document.body.appendChild(script);
};

const shouldAnimateTransition = (
    anchor: HTMLAnchorElement | URL | Location
): boolean => {
    if (anchor.host !== location.host) {
        // If target is on a different domain then handle it the normal way
        return false;
    }

    if (NoAnimationPathsRegex.test(anchor.pathname)) {
        return false;
    }

    // Links annotated with 'noanim' class should be treated as external (no content transition animations)
    if (
        anchor instanceof HTMLAnchorElement &&
        anchor.className.includes(NoAnimationClass)
    ) {
        return false;
    }

    return true;
};

const shouldScrollTo = (anchor: HTMLAnchorElement | URL | Location): boolean =>
    anchor.pathname === window.location.pathname &&
    anchor.search === window.location.search;

const setup = () => {
    // Intercept all click events
    document.addEventListener("click", e => {
        let el: HTMLElement | ParentNode = e.target as HTMLElement;

        // Go up in the nodelist until we find a node with .href (HTMLAnchorElement)
        while (el && !(el instanceof HTMLAnchorElement)) {
            el = el.parentNode;
        }

        if (!el) return;
        const anchor = el as HTMLAnchorElement;

        if (!shouldAnimateTransition(anchor)) return;

        if (anchor.hash && shouldScrollTo(anchor)) {
            // Handle links to element #id
            e.preventDefault();
            history.pushState(null, null, anchor.href);
            scrollToId(anchor.hash);
            return;
        }

        // Otherwise fetch content from the target and insert it
        // into the current page
        e.preventDefault();
        changePage(anchor.href);
    });

    window.addEventListener("popstate", () =>
        // Intercept 'back' events
        changePage(window.location.href, false)
    );

    window.addEventListener("load", () => {
        void onContentChanged(document);
        window.removeEventListener("load", this);
    });
};

export const changePage = (url: string, pushToHistory: boolean = true) => {
    if (pushToHistory) {
        history.pushState(null, null, url);
    }

    Scaffold.showLoading(true);

    loadPage(url)
        .then(responseText => {
            const wrapper = document.createElement("div");
            wrapper.innerHTML = responseText;

            document.title = wrapper.querySelector("title").textContent;
            getMetaDescription(document).content =
                getMetaDescription(wrapper).content;
            Scaffold.importLocalStyle(wrapper);

            const oldContent = Scaffold.getContent(document);
            const newContent = Scaffold.getContent(wrapper);

            animatePageChange(oldContent, newContent);
        })
        .catch(err => {
            console.error(err);
            window.location.href = url;
            Scaffold.showLoading(false);
        });
};

const getMetaDescription = (from: HTMLElement | Document) =>
    from.querySelector("meta[name=description]") as HTMLMetaElement;

const animatePageChange = (
    oldContent: HTMLElement,
    newContent: HTMLElement
) => {
    const fadeOut = oldContent.animate(
        [{ opacity: 1 }, { opacity: 0 }],
        PageAnimationDuration
    );

    fadeOut.onfinish = () => {
        const contentWrapper = Scaffold.getContentWrapper();
        contentWrapper.removeChild(oldContent);
        contentWrapper.appendChild(newContent);
        contentWrapper.scrollIntoView(true);

        Scaffold.showLoading(false);
        animateContentEnter(newContent);

        newContent
            .querySelectorAll(OnPageChangeClass)
            .forEach(executeContentScripts);
        oldContent
            .querySelectorAll(OnPageUnloadClass)
            .forEach(executeContentScripts);

        void onContentChanged(newContent);
    };
};

const executeContentScripts = (element: HTMLElement) => {
    const script = element as HTMLScriptElement;
    if (script.src) {
        void getScript(script);
    } else {
        try {
            eval(script.innerHTML);
        } catch (err) {}
    }
};

const animateContentEnter = (parent: HTMLElement) => {
    let delay = 0;

    try {
        parent.querySelectorAll(AnimatedElementSelector).forEach(el => {
            elementIn(el as HTMLElement, delay);

            delay += ItemAnimationDelay;
        });
    } catch (e) {}
};

const elementIn = (element: HTMLElement, delay: number) => {
    element.style.animationDelay = `${delay}ms`;
    element.dataset.animateIn = "true";
};

const scrollToId = (id: string) =>
    document.getElementById(id.replace("#", "")).scrollIntoView();

setup();
