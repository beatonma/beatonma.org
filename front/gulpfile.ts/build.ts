import { dest, parallel, series, src } from "gulp";
import gulpRename from "gulp-rename";
import { buildCss } from "./build-css";
import { buildJs } from "./build-js";
import { buildStatic } from "./build-static";
import { buildTemplates } from "./build-templates";
import { includeEnv } from "./env";
import { ANY_FILE, distPath } from "./paths";
import { checkConfiguration } from "./setup";

/**
 * Remove the `apps/` parent directory.
 */
export const unwrap = () =>
    gulpRename(path => {
        path.dirname = path.dirname.replace(/^apps\//, "");
    });

const injectEnvironmentVariables = () =>
    src(distPath(ANY_FILE)).pipe(includeEnv()).pipe(dest(distPath()));

export const rebuild = series(
    parallel(
        buildJs,
        buildCss,
        buildStatic,
        buildTemplates,
    ),
    injectEnvironmentVariables
);

export const completeBuild = series(checkConfiguration, rebuild);
