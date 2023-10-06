import { create as browserSyncCreate } from "browser-sync";
import { exec as shellExec } from "child_process";
import { sync as deleteSync } from "del";
import gulp, { dest, parallel, series, src } from "gulp";
import { ANY_FILE, distPath, djangoPath, localPath, srcPath } from "./paths";
import { build } from "./build";

const browserSync = browserSyncCreate();
const initBrowserSync = async () =>
    browserSync.init({
        proxy: "django:8000",
        open: false,
    });
const refreshBrowser = async () => {
    shellExec(`touch ${djangoPath("beatonma/__init__.py")}`);
    browserSync.reload();
};

const localDist = () => src(distPath(ANY_FILE)).pipe(dest(localPath()));
const localClean = async () => deleteSync(localPath(), { force: true });
const localBuild = series(
    parallel(build, localClean),
    localDist,
    refreshBrowser,
);

export const watch = series(localBuild, initBrowserSync, () =>
    gulp.watch(srcPath(ANY_FILE), localBuild),
);
