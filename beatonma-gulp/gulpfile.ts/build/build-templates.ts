import { srcPath } from "../paths";
import { isDevBuild } from "./config";
import { BuildStream, StreamWrapper } from "./types";
import { src } from "gulp";
import gulpIf from "gulp-if";
import { Transform } from "node:stream";
import Vinyl from "vinyl";

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
            callback: (error?: Error | null, data?: any) => void,
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

export const buildTemplates: BuildStream = (wrapper: StreamWrapper) =>
    function buildTemplates() {
        return wrapper(
            src(srcPath("**/*.html")).pipe(
                gulpIf(!isDevBuild(), minimiseWhitespace()),
            ),
        );
    };
