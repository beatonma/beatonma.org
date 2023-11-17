import { build } from "./build";
import {
    BuildOptionsFactory,
    initDev,
    initProduction,
    initTest,
} from "./build/config";
import { watch as _watch } from "./watch";
import { series } from "gulp";

const _dev = (options?: BuildOptionsFactory) =>
    series(function initDevBuild() {
        return initDev(options);
    }, _watch);
const nullBuild = (overrides: BuildOptionsFactory): BuildOptionsFactory =>
    Object.assign(
        {
            buildCss: false,
            buildWebapps: false,
            buildJs: false,
            buildStatic: false,
            buildTemplates: false,
            clean: true,
        },
        overrides,
    );

export const dev = _dev({ buildWebapps: false });
export const watch = dev;
export const devWithWebapps = _dev();
export const devCssOnly = _dev(nullBuild({ buildCss: true, clean: false }));
export const devJsOnly = _dev(nullBuild({ buildJs: true, clean: false }));
export const devWebappsOnly = _dev(
    nullBuild({ buildWebapps: true, clean: false }),
);

export const test = series(initTest, build);
export const production = series(initProduction, build);

export default dev;
