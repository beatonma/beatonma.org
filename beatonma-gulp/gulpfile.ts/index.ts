import { series } from "gulp";
import { initDev, initProduction, initTest } from "./build/config";
import { watch } from "./watch";
import { build } from "./build";

export const dev = series(initDev, watch);
export const test = series(initTest, build);
export const production = series(initProduction, build);

export default series(initDev, build);
