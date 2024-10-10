import { distPath } from "../paths";
import { getBuildOptions, isProductionBuild } from "./config";
import * as glob from "glob";

type Globs = string[];

export const assertOutputCorrect = async () => {
    const missingOutput: Globs = [];
    const checkFileExists = (path: string) => {
        const exists = glob.sync(distPath(path)).length === 1;
        if (!exists) missingOutput.push(path);
    };

    getExpectedFiles().forEach(checkFileExists);
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
    "static/icon/github.svg",
    "static/favicon/",
    "static/fonts/AppIcons.woff2",
    "static/fonts/RobotoMono-Regular.ttf",
    "static/fonts/Roboto-Regular.ttf",
    "static/images/mb.png",
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

/**
 * Files that are only required in production.
 */
const ExpectedProductionFiles: Globs = [
    "main/static/main/js/bma-*.LICENSE.txt",
    "main/static/main/js/bma-*.js.map",
];

const getExpectedFiles = () => {
    const options = getBuildOptions();
    const expected = [];

    if (options.buildCss) expected.push(...ExpectedCss);
    if (options.buildStatic) expected.push(...ExpectedStatic);
    if (options.buildJs) expected.push(...ExpectedJs);
    if (options.buildTemplates) expected.push(...ExpectedTemplates);

    return expected;
};
