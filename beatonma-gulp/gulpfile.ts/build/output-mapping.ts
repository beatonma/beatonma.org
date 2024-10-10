import { SpecialPath } from "../paths";
import { getEnvironment } from "./config";
import { DjangoApp, StaticResourceType } from "./types";
import gulpRename, { ParsedPath } from "gulp-rename";
import { join as joinPath } from "path";

/**
 * Redirect the file to the correct output path, based on its type and location
 * in the source filetree.
 */
export const mapToOutput = () =>
    gulpRename((path, file) => {
        if (file.isDirectory()) return;
        mapFileOutput(path, file.basename);
    });

const mapFileOutput = (path: ParsedPath, filename: string) => {
    const extension = filename.split(".").slice(1).join(".");
    const splitDirPath = path.dirname.split("/");
    const baseDirName = splitDirPath[0];

    path.dirname = splitDirPath.slice(1).join("/");

    const djangoAppMap: Record<string, DjangoApp> = {
        [SpecialPath.SourceRoot.Core]: "main",
        [SpecialPath.SourceRoot.Static]: "main",
        [SpecialPath.SourceRoot.DjangoApps]: splitDirPath[1],
    };
    const djangoAppName: DjangoApp = djangoAppMap[baseDirName];

    if (extension === "html") return mapTemplate(path, djangoAppName);
    return mapStaticFile(path, djangoAppName, extension);
};

const mapTemplate = (path: ParsedPath, app: DjangoApp) => {
    const relPath = path.dirname.replace(
        new RegExp(`^${app}/(templates/?)?`),
        "",
    );

    if (relPath.startsWith(SpecialPath.Templates.FlatPages)) {
        path.dirname = joinPath("templates", "flatpages");
        return;
    }

    if (relPath.startsWith(SpecialPath.Templates.RootTemplates)) {
        path.dirname = "templates/";
        return;
    }

    path.dirname = SpecialPath.Outputs.djangoTemplate(app, relPath);
};

/**
 * Direct the file to the correct static files directory.
 *
 * Javascript and CSS files are treated differently than others.
 * - Files are stored in a flat `js` or `css` directory, alongside related
 *   license and source-maps.
 * - The current git hash will be inserted into filenames.
 *
 * For other files, directory structure will be maintained from the source.
 */
const mapStaticFile = (path: ParsedPath, app: DjangoApp, extension: string) => {
    const StaticResourceMap: Record<string, StaticResourceType> = {
        css: "css",
        "css.map": "css",
        js: "js",
        "js.map": "js",
        "js.LICENSE.txt": "js",
    };
    const resourceType = StaticResourceMap[extension];

    if (resourceType) {
        path.dirname = SpecialPath.Outputs.djangoStatic(app, resourceType);
        path.basename = injectGitHash(path.basename);
        return;
    }

    path.dirname = joinPath(
        SpecialPath.Outputs.djangoStatic(app, null),
        path.dirname,
    );
};

const injectGitHash = (filename: string): string =>
    filename.replace(
        /(?<basename>[^.]+)(?<extension>\.?.*)/,
        `$1-${getEnvironment().gitHash}$2`,
    );
