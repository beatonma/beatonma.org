import { series } from "gulp";
import { completeBuild } from "./build";
import { watch, watchWebapp } from "./dist-watch";
import {
    getBuildMode as _getBuildType,
    initDev,
    initProduction,
    isProductionBuild as _isProductionBuild,
} from "./setup";

/**
 * Reduced local build with no minification, watched locally.
 */
export default series(initDev, watch);

/**
 * Complete build, nothing more.
 */
export const build = series(initProduction, completeBuild);

/**
 * Complete build with minification, watched locally.
 */
export const local = series(initProduction, watch);


export const getBuildType = _getBuildType;
export const isProductionBuild = _isProductionBuild;

export const webapp = series(initDev, watchWebapp);
