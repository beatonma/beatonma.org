import { distPath } from "../paths";
import { assertOutputCorrect } from "./assertions";
import { buildCss } from "./build-css";
import { buildJs } from "./build-js";
import { buildStatic } from "./build-static";
import { buildTemplates } from "./build-templates";
import { buildWebapps } from "./build-webapps";
import { getEnvironment, isProductionBuild } from "./config";
import { includeWebappArtifacts, mapToOutput } from "./output-mapping";
import { ignore } from "./transforms";
import { Env, StreamWrapper } from "./types";
import * as fs from "fs";
import { dest, parallel, series } from "gulp";
import gulpIf from "gulp-if";
import gulpReplace from "gulp-replace";

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
        "g",
    );

    return gulpIf(isProductionBuild(), gulpReplace(combinedPattern, ""));
};

/**
 * Inject __env__:key with value of env[key].
 */
const includeEnv = () => {
    const env = getEnvironment();

    return gulpReplace(/__env__:(\w+)/g, function (match: string, key: string) {
        if (key in env) {
            return env[key as keyof Env] as string;
        }
        throw `Unknown environment key '${key}'. (Keys: ${Object.keys(env).join(
            "",
        )})`;
    });
};

const filterUnwanted = ignore(file => {
    if (file.path.includes("node_modules")) return true;
    return file.isDirectory() && fs.readdirSync(file.path).length === 0;
});

/**
 * Apply common transforms to all build artifacts.
 */
const streamWrapper: StreamWrapper = stream =>
    stream
        .pipe(filterUnwanted())
        .pipe(includeEnv())
        .pipe(removeCypressTags())
        .pipe(mapToOutput())
        .pipe(dest(distPath()));

export const build = series(
    parallel(
        buildCss(streamWrapper),
        buildJs(streamWrapper),
        buildStatic(streamWrapper),
        buildTemplates(streamWrapper),
        buildWebapps(includeWebappArtifacts),
    ),
    assertOutputCorrect,
);
