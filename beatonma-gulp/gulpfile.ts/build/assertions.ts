import { distPath } from "../paths";
import { isProductionBuild } from "./config";
import * as glob from "glob";

type Globs = string[];

export const assertOutputCorrect = async () => {
    const checkFileExists = (path: string) => {
        const exists = glob.sync(distPath(path)).length === 1;
        if (!exists) missingOutput.push(path);
    };

    const missingOutput: Globs = [];
    ExpectedFileOutput.forEach(checkFileExists);
    if (isProductionBuild()) {
        ExpectedProductionFiles.forEach(checkFileExists);
    }

    if (missingOutput.length > 0) {
        throw `Expected output files were not found in build output:
- ${missingOutput.join("\n- ")}
`;
    }
};

const ExpectedStatic: Globs = [
    "main/static/main/icon/github.svg",
    "main/static/main/favicon/",
    "main/static/main/fonts/RobotoMono-Regular.ttf",
    "main/static/main/fonts/Roboto-Regular.ttf",
    "main/static/main/images/mb.png",
];

const ExpectedCss: Globs = [
    "dashboard/static/dashboard/css/dashboard-*.css",
    "main/static/main/css/admin-*.css",
    "main/static/main/css/bma-*.css",
    "main/static/main/css/staff-*.css",
];

const ExpectedJs: Globs = [
    "dashboard/static/dashboard/js/dashboard-*.js",
    "main/static/main/js/bma-*.js",
];

const ExpectedTemplates: Globs = [
    "contact/templates/contact.html",
    "main/templates/pages/about.html",
    "main/templates/pages/index/",
    "main/templates/pages/posts/",
    "main/templates/pages/search-results/",
    "templates/400.html",
    "templates/403.html",
    "templates/404.html",
    "templates/500.html",
    "templates/flatpages/default.html",
    "templates/flatpages/null.html",
    "mentions/templates/webmention-submit-manual.html",
    "webmentions_tester/templates/webmentions_tester.html",
];

const ExpectedWebapps: Globs = [
    "main/static/main/webapp/clocks.js",
    "main/static/main/webapp/palette.js",
];

/**
 * Files that are only required in production.
 */
const ExpectedProductionFiles: Globs = [
    "main/static/main/css/bma-*.css.map",
    "main/static/main/js/bma-*.LICENSE.txt",
    "main/static/main/js/bma-*.js.map",
];

const ExpectedFileOutput: Globs = [
    ...ExpectedStatic,
    ...ExpectedCss,
    ...ExpectedJs,
    ...ExpectedTemplates,
    ...ExpectedWebapps,
];
