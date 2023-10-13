/**
 * Special named paths which get specific treatment.
 *
 * If any of these paths change in the filetree they must also be updated here!
 */
import { DjangoApp, StaticResourceType } from "./build/types";
import * as path from "path";

const _distPath = process.env.GULP_OUTPUT_ROOT ?? "dist/";
const absoluteDistPath = _distPath.startsWith("/")
    ? _distPath
    : path.join(path.resolve("."), _distPath);

/**
 * Build a path relative to the root source directory.
 */
export const srcPath = (_path?: string) =>
    path.join(SpecialPath.Gulp.Source, _path ?? "");

/**
 * Build a path relative to the root output directory.
 */
export const distPath = (_path?: string) =>
    path.join(SpecialPath.Gulp.Dist, _path ?? "");

const djangoStatic = (appName: DjangoApp, type: StaticResourceType): string => {
    const root = `${appName}/static/${appName}`;
    if (type) return `${root}/${type}/`;
    return root;
};

const djangoTemplate = (appName: DjangoApp, path: string) => {
    if (appName) return `${appName}/templates/${path}`;
    return `templates/${path}`;
};

/**
 * Names of any special directories that get some sort of specific treatment
 * during the Gulp build process.
 *
 * Any changes in the source filetree must be reflected here.
 */
export const SpecialPath = {
    Gulp: {
        Source: "src/",
        Dist: _distPath,
    },

    Templates: {
        FlatPages: "pages/__root__/flatpages",
        RootTemplates: "pages/__root__/",
    },

    /**
     * Names of special top-level directories within the gulp sources root..
     */
    SourceRoot: {
        /**
         * Name of the root directory of the main web app.
         */
        Core: "core",
        /**
         * Name of the root directory of Django app resources.
         */
        DjangoApps: "django_apps",
        /**
         * Name of the root directory of standalone webapps.
         */
        WebApps: "webapp",
        /**
         * Name of the root directory of generic static files.
         */
        Static: "static",
    },

    Outputs: {
        djangoTemplate: djangoTemplate,
        djangoStatic: djangoStatic,
        djangoWebapp: path.join(
            absoluteDistPath,
            djangoStatic("main", "webapp"),
        ),
    },
};
