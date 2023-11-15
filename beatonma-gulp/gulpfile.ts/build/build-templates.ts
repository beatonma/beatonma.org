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
    return new Transform({
        objectMode: true,
        transform(
            file: Vinyl,
            encoding: BufferEncoding,
            callback: (error?: Error | null, data?: any) => void,
        ) {
            if (file.isNull()) return callback(null, file);

            if (file.isBuffer()) {
                file.contents = Buffer.from(
                    _minimiseWhitespace(String(file.contents)),
                );
                return callback(null, file);
            }
            callback(TypeError(`Unhandled file: ${file}`));
        },
    });
};

const Whitespace = {
    afterDjangoTag: /(?<=%})\s+(?=[<{])/gs, // After Django tag if followed by another Django or HTML tag
    endOfHtmlTag: /(?<!{.*?)(?<=<.*?)\s+(?=\/?>)/gs, // Before closing > or />
    atLineStart: /^\s+/gm,
    lineBreaksInHtmlTag: /(?<=<[^>]+)[\r\n]+/gs,
    repeatedSpaces: / {2,}/g,
    linebreaks: /\s*\n\s*/gms,
};
const _minimiseWhitespace = (content: string): string => {
    const removeAll = combineRegex(
        Whitespace.atLineStart,
        Whitespace.endOfHtmlTag,
        Whitespace.afterDjangoTag,
    );

    const replaceSpace = combineRegex(
        Whitespace.repeatedSpaces,
        Whitespace.lineBreaksInHtmlTag,
    );

    return content
        .replace(Whitespace.linebreaks, "\n")
        .replace(removeAll, "")
        .replace(replaceSpace, " ");
};

const combineRegex = (...regex: RegExp[]) => {
    const sources: string[] = [];
    const flags: Set<string> = new Set();
    for (let i = 0; i < regex.length; i++) {
        const r = regex[i];
        sources.push(r.source);
        [...r.flags].forEach(it => flags.add(it));
    }

    return new RegExp(sources.join("|"), [...flags].join(""));
};

export const buildTemplates: BuildStream = (wrapper: StreamWrapper) =>
    function buildTemplates() {
        return wrapper(
            src(srcPath("**/*.html")).pipe(
                gulpIf(!isDevBuild(), minimiseWhitespace()),
            ),
        );
    };

export const ExportForTesting = {
    WhitespacePatterns: Whitespace,
    minimiseWhitespace: _minimiseWhitespace,
};
