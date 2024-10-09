import { SpecialPath, srcPath } from "../paths";
import { isDevBuild } from "./config";
import { BuildStream, StreamWrapper } from "./types";
import autoprefixer from "autoprefixer";
import cssnano from "cssnano";
import { src } from "gulp";
import gulpIf from "gulp-if";
import gulpPostCss from "gulp-postcss";
import gulp_sass from "gulp-sass";
import sass from "sass";

const gulpSass = gulp_sass(sass);

export const buildCss: BuildStream = (wrapper: StreamWrapper) =>
    function buildCss() {
        return wrapper(
            src(srcPath("**/*.scss"))
                .pipe(
                    gulpSass({
                        includePaths: [srcPath(SpecialPath.SourceRoot.Core)],
                    }),
                )
                .pipe(
                    gulpIf(
                        isDevBuild(),
                        gulpPostCss([autoprefixer()]),
                        gulpPostCss([autoprefixer(), cssnano()]),
                    ),
                ),
        );
    };
