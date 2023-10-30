import { srcPath } from "../paths";
import { getWebpackBuildMode } from "./config";
import { BuildStream, StreamWrapper } from "./types";
import { shell_command } from "./util";
import { parallel, src } from "gulp";
import Vinyl from "vinyl";
import named from "vinyl-named";
import { Configuration } from "webpack";
import webpackStream from "webpack-stream";

type WebpackBuildMode = "development" | "production";
const EntryPoints = ["**/bma.ts", "**/dashboard.tsx"].map(srcPath);

/**
 * Without this, webpackStream forgets where the file originated which causes
 * problems when trying to decide where to put it later.
 */
const keepName = () =>
    named((file: Vinyl) => file.relative.replace(/.tsx?$/, ""));

/**
 * This is called from gulp - not a valid standalone webpack configuration file.
 */
const getWebpackConfig = (
    mode: WebpackBuildMode = getWebpackBuildMode(),
): Configuration => {
    const isProduction = mode === "production";

    return {
        mode: mode,
        devtool: isProduction ? "source-map" : "inline-source-map",
        optimization: {
            minimize: isProduction,
        },
        output: {
            filename: "[name].js",
        },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: "swc-loader",
                    },
                },
            ],
        },
        resolve: {
            extensions: [".ts", ".tsx"],
        },
    };
};

const _buildJs: BuildStream = (wrapper: StreamWrapper) =>
    function buildJs() {
        const config = getWebpackConfig();
        return wrapper(
            src(EntryPoints).pipe(keepName()).pipe(webpackStream(config)),
        );
    };

const checkTypescript = () =>
    shell_command("tsc --project ./tsconfig.json --noEmit");

export const buildJs = (wrapper: StreamWrapper) =>
    parallel(_buildJs(wrapper), checkTypescript);
