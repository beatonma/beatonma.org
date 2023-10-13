import { srcPath } from "../paths";
import { BuildStream, StreamWrapper } from "./types";
import { src } from "gulp";

export const buildStatic: BuildStream = (wrapper: StreamWrapper) =>
    function collectStatic() {
        return wrapper(src(srcPath("**/static/**")));
    };
