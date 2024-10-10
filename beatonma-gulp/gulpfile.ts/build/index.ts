import { distPath } from "../paths";
import { assertOutputCorrect } from "./assertions";
import { buildCss } from "./build-css";
import { buildJs } from "./build-js";
import { buildStatic } from "./build-static";
import { buildTemplates } from "./build-templates";
import { getBuildOptions, getEnvironment, isProductionBuild } from "./config";
import { mapToOutput } from "./output-mapping";
import { ignore } from "./transforms";
import { Env, StreamWrapper } from "./types";
import * as fs from "fs";
import { dest, parallel, series } from "gulp";
import gulpIf from "gulp-if";
import gulpReplace from "gulp-replace";
import Vinyl from "vinyl";

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

/**
 * Remove empty directories from output.
 */
const filterUnwanted = ignore(file => {
    return file.isDirectory() && fs.readdirSync(file.path).length === 0;
});

const isTextFile = (file: Vinyl): boolean => {
    return [".txt", ".md", ".html", ".js", ".css"].includes(file.extname);
};

/**
 * Apply common transforms to all build artifacts.
 */
const streamWrapper: StreamWrapper = stream =>
    stream
        .pipe(filterUnwanted())
        .pipe(gulpIf(isTextFile, includeEnv()))
        .pipe(gulpIf(isTextFile, removeCypressTags()))
        .pipe(mapToOutput())
        .pipe(dest(distPath()));

const buildTasks = (callback: () => void) => {
    const options = getBuildOptions();
    const tasks = [
        options.buildCss ? buildCss(streamWrapper) : null,
        options.buildJs ? buildJs(streamWrapper) : null,
        options.buildStatic ? buildStatic(streamWrapper) : null,
        options.buildTemplates ? buildTemplates(streamWrapper) : null,
    ].filter(Boolean);

    if (tasks.length === 0)
        throw "All build tasks have been disabled by options!";
    return parallel(...tasks)(callback);
};

export const build = series(buildTasks, assertOutputCorrect);
