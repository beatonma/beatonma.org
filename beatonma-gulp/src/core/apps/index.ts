import { ContactApp } from "./contact";
import { MediaViewerApp } from "./media-viewer";
import { WebmentionsApp } from "./webmentions";
import { GithubEventsApp } from "./github-events";
import { WebmentionTesterApp } from "./webmentions-tester";
import "./search";

/**
 * Apps which render as part of the page content.
 */
export const LocalApps = [
    MediaViewerApp,
    GithubEventsApp,
    ContactApp,
    WebmentionsApp,
    WebmentionTesterApp,
];
