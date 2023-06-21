import { dest, parallel, src } from "gulp";
import {distPath, srcPath} from "./paths";
import { unwrap } from "./build";
import gulpRename from "gulp-rename";

const collectStatic = () =>
    src(srcPath("static/**/*")).pipe(dest(distPath("main/static/main/")));

const collectImages = () =>
    src(srcPath("**/images/**/*"))
        .pipe(
            gulpRename(path => {
                // Move to apps/appname/static/appname/images
                path.dirname = path.dirname.replace(
                    /apps[/\\](.+?)[/\\]images/g,
                    "apps/$1/static/$1/images"
                );
            })
        )
        .pipe(unwrap())
        .pipe(dest(distPath()));

export const buildStatic = parallel(collectStatic, collectImages);
