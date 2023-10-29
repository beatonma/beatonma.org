import { srcPath } from "../paths";
import { getWebpackBuildMode } from "./config";
import { BuildStream, StreamWrapper } from "./types";
import { shell_command } from "./util";
import { getConfig } from "./webpack.config";
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
    shell_command("tsc --project ./tsconfig.json --noEmit");

export const buildJs = (wrapper: StreamWrapper) =>
    parallel(_buildJs(wrapper), checkTypescript);
