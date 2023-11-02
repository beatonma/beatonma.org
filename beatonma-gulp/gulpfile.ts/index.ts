import { build } from "./build";
import {
    BuildOptionsFactory,
    initDev,
    initProduction,
    initTest,
} from "./build/config";
import { watch } from "./watch";
import { series } from "gulp";

const _dev = (options?: BuildOptionsFactory) =>
    series(function initDevBuild() {
        return initDev(options);
    }, watch);
export const dev = _dev({ buildWebapps: false });
export const devWithWebapps = _dev();

export const test = series(initTest, build);
export const production = series(initProduction, build);

export default dev;
