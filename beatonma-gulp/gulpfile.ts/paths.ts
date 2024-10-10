/**
 * Special named paths which get specific treatment.
 *
 * If any of these paths change in the filetree they must also be updated here!
 */
import { DjangoApp, StaticResourceType } from "./build/types";
import { join as joinPath } from "path";

const gulpDistPath = process.env.GULP_OUTPUT_ROOT ?? "dist/";

/**
 * Build a path relative to the root source directory.
 */
export const srcPath = (_path?: string) =>
    joinPath(SpecialPath.Gulp.Source, _path ?? "");

/**
 * Build a path relative to the root output directory.
 */
export const distPath = (_path?: string) =>
    joinPath(SpecialPath.Gulp.Dist, _path ?? "");

const djangoStatic = (appName: DjangoApp, type: StaticResourceType): string => {
    const root = joinPath(appName, "static", appName);
    if (type) return joinPath(root, type);
    return root;
};

const djangoTemplate = (appName: DjangoApp, path: string) => {
    if (appName) return joinPath(appName, "templates", path);
    return joinPath("templates", path);
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
        Dist: gulpDistPath,
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
         * Name of the root directory of generic static files.
         */
        Static: "static",
    },

    Outputs: {
        djangoTemplate: djangoTemplate,
        djangoStatic: djangoStatic,
        Static: "static",
    },
};
