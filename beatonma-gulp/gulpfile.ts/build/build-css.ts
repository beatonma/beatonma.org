import { SpecialPath, srcPath } from "../paths";
import { isDevBuild } from "./config";
import { ignore } from "./transforms";
import { BuildStream, StreamWrapper } from "./types";
import autoprefixer from "autoprefixer";
import cssnano from "cssnano";
import { src } from "gulp";
import gulpIf from "gulp-if";
import gulpPostCss from "gulp-postcss";
import gulp_sass from "gulp-sass";
import gulpSourcemaps from "gulp-sourcemaps";
import sass from "sass";

const gulpSass = gulp_sass(sass);

/**
 * Webapps-specific styles should not be a part of main stylesheet.
 * Instead, they should import their styles into their javascript application.
 */
const ignoreWebapps = ignore(file =>
    file.relative.startsWith(SpecialPath.SourceRoot.WebApps),
);

export const buildCss: BuildStream = (wrapper: StreamWrapper) =>
    function buildCss() {
        return wrapper(
            src(srcPath("**/*.scss"))
                .pipe(ignoreWebapps())
                .pipe(
                    gulpSass({
                        includePaths: [srcPath(SpecialPath.SourceRoot.Core)],
                    }),
                )
                .pipe(gulpSourcemaps.init())
                .pipe(
                    gulpIf(
                        isDevBuild(),
                        gulpPostCss([autoprefixer()]),
                        gulpPostCss([autoprefixer(), cssnano()]),
                    ),
                )
                .pipe(gulpSourcemaps.write(".")),
        );
    };
