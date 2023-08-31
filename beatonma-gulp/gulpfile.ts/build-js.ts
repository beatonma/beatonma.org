import { distPath, srcPath } from "./paths";
import { dest, parallel, src } from "gulp";
import { exec as shellExec } from "child_process";
import webpackStream from "webpack-stream";
import { getConfig } from "../webpack.config";
import named from "vinyl-named";
import Vinyl from "vinyl";
import { unwrap } from "./build";
import { getGitHash, getWebpackBuildMode } from "./setup";

const EntryPoints = [
    "**/app.ts",
    "**/dashboard.tsx",
    "**/entrypoint.ts",
    "**/entrypoint.tsx",
].map(pattern => srcPath(pattern));

const renameForWebpack = () =>
    named((file: Vinyl) => {
        const original = file.history[0];
        const matches = original.match(/.*\/([^/]+)\/js\/(.*)\.tsx?/);
        if (matches) {
            const appname = matches[1];
            const filename = matches[2];

            return `${appname}/static/${appname}/js/${filename}-${getGitHash()}.min`;
        }

        const webappMatches = original.match(
            /^.*\/webapp\/([\w-]+)\/(js\/)?entrypoint\.tsx?$/
        );
        if (!webappMatches) {
            throw `Unexpected structure for entrypoint: ${original}`;
        }

        const appname = webappMatches[1];
        return `webapp/static/${appname}/js/${appname}-${getGitHash()}.min`;
    });

const _buildJs = () =>
    src(EntryPoints)
        .pipe(renameForWebpack())
        .pipe(webpackStream(getConfig(getWebpackBuildMode())))
        .pipe(unwrap())
        .pipe(dest(distPath()));

const checkTypescript = async () => {
    shellExec(
        "tsc --project ./tsconfig.json --noEmit",
        (error, stdout, stderr) => {
            if (error) {
                console.error("Typescript error", error);
                if (stderr) console.error(stderr);
                if (stdout) console.error(stdout);
            }
        }
    );
};

export const buildJs = parallel(_buildJs, checkTypescript);
