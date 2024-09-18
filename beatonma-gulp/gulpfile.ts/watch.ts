import { build } from "./build";
import { srcPath } from "./paths";
import { create as browserSyncCreate } from "browser-sync";
import { exec as shellExec } from "child_process";
import gulp, { series } from "gulp";

const browserSync = browserSyncCreate();
const initBrowserSync = async () =>
    browserSync.init({
        proxy: "django:8000",
        open: false,
        middleware: (req, res, next) => {
            res.setHeader("Access-Control-Allow-Origin", "*");
            next();
        },
    });
const refreshBrowser = async () => {
    shellExec(`touch ${process.env.DJANGO_ROOT}beatonma/__init__.py`);
    browserSync.reload();
};

const localBuild = series(build, refreshBrowser);

export const watch = series(localBuild, initBrowserSync, () =>
    gulp.watch(
        [srcPath("**"), "!**/node_modules/**", "!**/dist/**"],
        localBuild,
    ),
);
