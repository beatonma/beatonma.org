/**
 * Expected structure:
 *
 *   <div id="{contentWrapperID}>
 *     <div id="{contentID}">
 *       <!-- Animated content here -->
 *     </div>
 *   </div>
 */
import { LocalApps } from "../apps";
import { loadPage } from "../util/requests";
import { Scaffold } from "./dom";

const AnimationMillis = {
    ItemDelay: 30,
    PageFadeOutDuration: 200,
};
// Links with this class opt out of hot-swapping content.
const NoAnimationClass = "noanim";

// Disable animations when the URL path matches this pattern.
const NoAnimationPathsRegex = /(webapp)\/.*/;

const DataAttr = {
    AnimateIn: "data-animate-in",
    Href: "data-href",
};

const Selector = {
    AnimatedElement: [
        ".card",
        ".h-card",
        ".h-entry",
        "article > section",
        "main > article",
    ].join(","),
    OnPageChange: ".onPageChange",
    OnPageUnload: ".onPageUnload",
};

export const animatedItemProps = (index: number) => {
    return {
        [DataAttr.AnimateIn]: true,
        style: {
            animationDelay: `${AnimationMillis.ItemDelay * index}ms`,
        },
    };
};

export const changePage = (url: string, pushToHistory: boolean = true) => {
    if (pushToHistory) {
        history.pushState(null, null, url);
    }

    Scaffold.showLoading(true);

    // Remove focus from the current element, allowing  any overlays that
    // use `focus-within` (e.g. search UI) to get out of the way.
    (document.activeElement as HTMLElement).blur();

    loadPage(url)
        .then(swapPageContent)
        .catch(err => {
            console.error(err);
            window.location.href = url;
            Scaffold.showLoading(false);
        });
};

const onContentChanged = async (dom: Document | HTMLElement) => {
    LocalApps.forEach(app => {
        try {
            app(dom);
        } catch (e) {
            console.error(`App '${app.name}' failed: ${e}`);
        }
    });

    if (window.location.hash) {
        scrollToId(window.location.hash);
    }
};

const getMetaDescription = (from: HTMLElement | Document): HTMLMetaElement =>
    from.querySelector("meta[name=description]") as HTMLMetaElement;

const swapPageContent = (newHtml: string) => {
    const wrapper = document.createElement("div");
    wrapper.innerHTML = newHtml;

    const oldContent = Scaffold.getContent(document);
    const newContent = Scaffold.getContent(wrapper);

    const fadeOut = oldContent.animate(
        [{ opacity: 1 }, { opacity: 0 }],
        AnimationMillis.PageFadeOutDuration,
    );

    fadeOut.onfinish = () => {
        document.title = wrapper.querySelector("title").textContent;
        getMetaDescription(document).content =
            getMetaDescription(wrapper).content;
        Scaffold.importLocalStyle(wrapper);

        const contentWrapper = Scaffold.getContentWrapper();
        contentWrapper.replaceChild(newContent, oldContent);
        contentWrapper.scrollIntoView(true);

        Scaffold.showLoading(false);

        newContent
            .querySelectorAll(Selector.OnPageChange)
            .forEach(ContentScripts.execute);
        oldContent
            .querySelectorAll(Selector.OnPageUnload)
            .forEach(ContentScripts.execute);

        animateContentEnter(newContent);
        void onContentChanged(newContent);
    };
};

namespace ContentScripts {
    export const execute = (element: HTMLElement) => {
        const script = element as HTMLScriptElement;
        if (script.src) {
            void getScript(script);
        } else {
            try {
                eval(script.innerHTML);
            } catch (err) {
                console.error(`Page-change script error: ${err}`);
            }
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
}

const animateContentEnter = (parent: HTMLElement) => {
    let delay = 0;

    try {
        parent.querySelectorAll(Selector.AnimatedElement).forEach(el => {
            const element = el as HTMLElement;
            element.style.animationDelay = `${delay}ms`;
            element.dataset.animateIn = "true";

            delay += AnimationMillis.ItemDelay;
        });
    } catch (e) {
        console.warn(`Animation error: ${e}`);
    }
};

const scrollToId = (id: string) => {
    const resolvedId = id.replace("#", "");
    const target = document.getElementById(resolvedId);
    target.scrollIntoView();
    if (resolvedId !== Scaffold.ContentId) {
        target.dataset.highlighted = "true";
    }
};

namespace PageTransitionEvents {
    const onClick = (e: MouseEvent) => {
        const target = findNavigableTarget(e);
        if (!target) return;
        const { url, shouldAnimate } = target;
        if (!shouldAnimate) return;

        if (url.hash && shouldScrollTo(url)) {
            // Handle links to element #id
            e.preventDefault();
            history.pushState(null, null, url.href);
            scrollToId(url.hash);
            return;
        }

        // Otherwise fetch content from the target and insert it
        // into the current page
        e.preventDefault();
        changePage(url.href);
    };

    const onNavigateBack = () => changePage(window.location.href, false);

    function onLoad() {
        void onContentChanged(document);
        window.removeEventListener("load", this);
    }

    export const setup = () => {
        document.addEventListener("click", onClick);
        window.addEventListener("popstate", onNavigateBack);
        window.addEventListener("load", onLoad);
    };

    interface Navigable {
        url: URL;
        shouldAnimate: boolean;
    }
    const findNavigableTarget = (event: Event): Navigable | null => {
        let el: HTMLElement = event.target as HTMLElement;
        let url: URL;

        while (el && !(el instanceof HTMLBodyElement)) {
            if (el instanceof HTMLAnchorElement) {
                url = new URL(el.href);
                break;
            }
            if ((el as HTMLElement).hasAttribute(DataAttr.Href)) {
                url = new URL(el.getAttribute(DataAttr.Href));
                break;
            }
            el = el.parentNode as HTMLElement;
        }

        if (el && url) {
            return {
                url: url,
                shouldAnimate: shouldAnimateTransition(url, el),
            };
        }

        return null;
    };

    const shouldAnimateTransition = (
        url: URL,
        element: HTMLElement,
    ): boolean => {
        if (url.host !== location.host) {
            // If target is on a different domain then handle it the normal way
            return false;
        }

        if (NoAnimationPathsRegex.test(url.pathname)) {
            return false;
        }

        // Links annotated with NoAnimationClass should be treated as external (no content transition animations)
        if (element.className.includes(NoAnimationClass)) {
            return false;
        }

        return true;
    };

    const shouldScrollTo = (anchor: URL): boolean =>
        anchor.pathname === window.location.pathname &&
        anchor.search === window.location.search;
}

PageTransitionEvents.setup();
