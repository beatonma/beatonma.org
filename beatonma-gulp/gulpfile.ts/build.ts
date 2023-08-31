import { dest, parallel, series, src } from "gulp";
import gulpIf from "gulp-if";
import gulpRename from "gulp-rename";
import gulpReplace from "gulp-replace";
import { buildCss } from "./build-css";
import { buildJs } from "./build-js";
import { buildStatic } from "./build-static";
import { buildTemplates } from "./build-templates";
import { Env } from "./env";
import { ANY_FILE, distPath } from "./paths";
import { getEnvironment, isProductionBuild } from "./setup";

/**
 * HTML elements that are targets for Cypress tests are tagged with `data-cy`
 * attributes which should not be included in the final production build.
 *
 * These elements may be found in HTML template files, or in compiled React files.
 */
const removeCypressTags = () => {
    const htmlPattern = new RegExp(`data-cy=".*?"`);
    const reactPattern = new RegExp(`"data-cy":\\s*?.*?".*?",?`);
    const combinedPattern = new RegExp(
        `${htmlPattern.source}|${reactPattern.source}`,
        "g"
    );

    return gulpIf(
        isProductionBuild(),
        gulpReplace(combinedPattern, (match, key) => {
            console.debug(`Removed '${match}'`);
            return "";
        })
    );
};

/**
 * Inject __env__:key with value of env[key].
 */
const includeEnv = () => {
    const env = getEnvironment();

    return gulpReplace(/__env__:(\w+)/g, function (match: string, key: string) {
        if (Object.keys(env).includes(key)) {
            console.debug(
                `__env__:${key} -> '${env[key as keyof Env]}' | ${
                    this.file.basename
                }`
            );
            return env[key as keyof Env] as string;
        } else {
            throw `Unknown environment key ${key}`;
        }
    });
};

const applyGlobalTransformations = () =>
    src(distPath(ANY_FILE))
        .pipe(includeEnv())
        .pipe(removeCypressTags())
        .pipe(dest(distPath()));

/**
 * Remove the `apps/` parent directory.
 */
export const unwrap = () =>
    gulpRename(path => {
        path.dirname = path.dirname.replace(/^apps\//, "");
    });

export const build = series(
    parallel(buildJs, buildCss, buildStatic, buildTemplates),
    applyGlobalTransformations
);
