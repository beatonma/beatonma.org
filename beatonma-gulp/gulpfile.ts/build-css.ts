import autoprefixer from "autoprefixer";
import gulp_sass from "gulp-sass";
import sass from "sass";
import { dest, src } from "gulp";
import { distPath, srcPath } from "./paths";
import gulpRename from "gulp-rename";
import gulpSourcemaps from "gulp-sourcemaps";
import gulpIf from "gulp-if";
import { getGitHash, isDevBuild } from "./setup";
import gulpPostCss from "gulp-postcss";
import cssnano from "cssnano";
import { unwrap } from "./build";

const gulpSass = gulp_sass(sass);

/**
 * Inject the current git hash to the name of any minified files.
 */
const appendGitHashToFilename = () =>
    gulpRename(path => {
        path.basename = path.basename.replace(
            /([^.]+)(\.?.*)/,
            `$1-${getGitHash()}$2.min`
        );
    });

export const buildCss = () =>
    src(srcPath("**/scss/**/*.scss"))
        .pipe(gulpSass())
        .pipe(appendGitHashToFilename())
        .pipe(gulpSourcemaps.init())
        .pipe(
            gulpIf(
                isDevBuild(),
                gulpPostCss([autoprefixer()]),
                gulpPostCss([autoprefixer(), cssnano()])
            )
        )
        .pipe(gulpSourcemaps.write("."))
        .pipe(
            gulpRename(path => {
                // Move to apps/appname/static/appname/css
                path.dirname = path.dirname.replace(
                    /apps\/(.+?)\/scss/g,
                    "apps/$1/static/$1/css"
                );
            })
        )
        .pipe(unwrap())
        .pipe(dest(distPath()));
