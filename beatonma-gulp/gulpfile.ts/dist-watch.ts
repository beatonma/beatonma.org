import { create as browserSyncCreate } from "browser-sync";
import { exec as shellExec } from "child_process";
import del from "del";
import gulp, { parallel } from "gulp";
import { completeBuild } from "./build";
import { buildJs } from "./build-js";
import { ANY_FILE, distPath, djangoPath, localPath, srcPath } from "./paths";

const { src, dest, series } = gulp;

const browserSync = browserSyncCreate();

const initBrowser = async () =>
    browserSync.init({
        proxy: "django:8000",
        open: false,
    });

const refreshBrowser = async () => {
    await (() => {
        // Encourage the dev server to update for any altered template files.
        // This path depends on docker compose volume configuration!
        shellExec(`touch ${djangoPath("beatonma/__init__.py")}`);
    })();
    browserSync.reload();
};

/**
 * Copy constructed files to our local Django project directory.
 */
const localDist = () => src(distPath(ANY_FILE)).pipe(dest(localPath()));

const clean = async () => {
    del.sync(localPath(), { force: true });
};

const localBuild = series(
    parallel(completeBuild, clean),
    localDist,
    refreshBrowser
);

const _watch = () => gulp.watch(srcPath(ANY_FILE), localBuild);

export const watch = series(localBuild, initBrowser, _watch);

const _watchWebapp = () =>
    gulp.watch(
        srcPath("**/webapp/**/*"),
        series(buildJs, localDist, async () => browserSync.reload())
    );
export const watchWebapp = series(
    initBrowser,
    buildJs,
    localDist,
    _watchWebapp
);
