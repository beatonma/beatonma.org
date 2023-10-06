import { dest, src } from "gulp";
import gulpIf from "gulp-if";
import gulpRename from "gulp-rename";
import Vinyl from "vinyl";
import { unwrap } from "./build";
import { ANY_HTML, distPath, srcPath } from "./paths";
import { isDevBuild } from "./setup";
import { Transform } from "node:stream";

const isRootTemplate = (file: Vinyl): boolean => {
    const path = file.history[0];
    return /.*root\/.*/.test(path);
};

/**
 * Copy error templates
 */
const collectRootPages = () =>
    gulpIf(
        isRootTemplate,
        gulpRename(path => {
            if (path.dirname.endsWith("flatpages")) {
                path.dirname = "templates/flatpages";
            } else if (path.dirname.endsWith("http_errors")) {
                path.dirname = "templates/";
            } else {
                path.dirname = path.dirname.replace(
                    /.*pages\/root/,
                    "templates/"
                );
            }
        })
    );

/**
 * Template source files should optimise for maintainability, but that can
 * result in silly amounts of whitespace in the final HTML files after extend,
 * include, etc.
 *
 * Not that it really matters, but it looks untidy.
 * Anyway, here we remove most of that whitespace, resulting in HTML source
 * that keeps the basic structure of the document intact but without any
 * indentations or gaps.
 */
const minimiseWhitespace = (): NodeJS.ReadWriteStream => {
    const afterDjangoTag = /(%})\s+/gs;
    const inHtmlTag = /(?<=<.*?)\s+(?=[^<]*>)/gs;
    const atLineStart = /^\s+/gm;
    const repeatedLineBreaks = /[\r\n]{2,}/g;

    return new Transform({
        objectMode: true,
        transform(
            file: Vinyl,
            encoding: BufferEncoding,
            callback: (error?: Error | null, data?: any) => void
        ) {
            if (file.isNull()) return callback(null, file);

            if (file.isBuffer()) {
                const contents = String(file.contents)
                    .replace(afterDjangoTag, "$1")
                    .replace(inHtmlTag, " ")
                    .replace(atLineStart, "")
                    .replace(repeatedLineBreaks, "\n");
                file.contents = Buffer.from(contents);
                return callback(null, file);
            }
            callback(TypeError(`Unhandled file: ${file}`));
        },
    });
};

export const buildTemplates = () =>
    src([srcPath(ANY_HTML), srcPath("**/templates/**/*.svg")])
        .pipe(gulpIf(!isDevBuild(), minimiseWhitespace()))
        .pipe(collectRootPages())
        .pipe(unwrap())
        .pipe(dest(distPath()));
