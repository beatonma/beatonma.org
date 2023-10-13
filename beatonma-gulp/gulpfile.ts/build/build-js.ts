import { srcPath } from "../paths";
import { getWebpackBuildMode } from "./config";
import { BuildStream, StreamWrapper } from "./types";
import { getConfig } from "./webpack.config";
import * as child_process from "child_process";
import { parallel, src } from "gulp";
import Vinyl from "vinyl";
import named from "vinyl-named";
import webpackStream from "webpack-stream";

const EntryPoints = ["**/bma.ts", "**/dashboard.tsx"].map(srcPath);

/**
 * Without this, webpackStream forgets where the file originated which causes
 * problems when trying to decide where to put it later.
 */
const keepName = () =>
    named((file: Vinyl) => file.relative.replace(/.tsx?$/, ""));

const _buildJs: BuildStream = (wrapper: StreamWrapper) =>
    function buildJs() {
        const config = getConfig(getWebpackBuildMode());
        return wrapper(
            src(EntryPoints).pipe(keepName()).pipe(webpackStream(config)),
        );
    };

const checkTypescript = () =>
    new Promise<void>((resolve, reject) => {
        child_process.exec(
            "tsc --project ./tsconfig.json --noEmit",
            (error, stdout, stderr) => {
                if (error) {
                    console.error("Typescript error", error);
                    if (stderr) console.error(stderr);
                    if (stdout) console.error(stdout);
                    return reject(error);
                }
                resolve();
            },
        );
    });

export const buildJs = (wrapper: StreamWrapper) =>
    parallel(_buildJs(wrapper), checkTypescript);
