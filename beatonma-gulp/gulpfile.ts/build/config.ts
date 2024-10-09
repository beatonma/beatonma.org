import { distPath } from "../paths";
import { Env } from "./types";
import { sync as deleteSync } from "del";

enum BuildMode {
    Development = "development",
    Production = "production",
    Test = "test",
}
interface BuildOptions {
    buildCss: boolean;
    buildJs: boolean;
    buildTemplates: boolean;
    buildStatic: boolean;
    clean: boolean;
}
export interface BuildOptionsFactory {
    buildCss?: boolean;
    buildJs?: boolean;
    buildTemplates?: boolean;
    buildStatic?: boolean;
    clean?: boolean;
}
let buildMode: BuildMode = null;
let environment: Env = null;
let buildOptions: BuildOptions = null;

export const getBuildOptions = () => buildOptions;
export const getEnvironment = () => environment;
export const getWebpackBuildMode = (): "development" | "production" =>
    buildMode === BuildMode.Test ? BuildMode.Production : buildMode;

export const isDevBuild = (): boolean => buildMode === BuildMode.Development;
export const isProductionBuild = (): boolean =>
    buildMode === BuildMode.Production;
export const isTestBuild = (): boolean => buildMode === BuildMode.Test;

export const initDev = async (options?: BuildOptionsFactory) =>
    init(BuildMode.Development, options);
export const initTest = async () => init(BuildMode.Test);
export const initProduction = async () => init(BuildMode.Production);

const init = async (mode: BuildMode, options?: BuildOptionsFactory) => {
    buildMode = mode;
    buildOptions = {
        buildCss: options?.buildCss ?? true,
        buildJs: options?.buildJs ?? true,
        buildTemplates: options?.buildTemplates ?? true,
        buildStatic: options?.buildStatic ?? true,
        clean: options?.clean ?? true,
    };
    environment = {
        gitHash: process.env.GIT_HASH ?? "__no_env__",
        contactEmail: process.env.WEBMAIL_CONTACT_EMAIL ?? "__no_env__",
        googleRecaptchaToken:
            process.env.GOOGLE_RECAPTCHA_TOKEN ?? "__no_env__",
        siteName: process.env.SITE_NAME ?? "__no_env__",
    };
    if (buildOptions.clean) {
        clean();
    }
    printConfig();
};

const clean = () => deleteSync([distPath("**")], { force: true });
const printConfig = () => {
    const stringify = (obj: any) =>
        JSON.stringify(obj, null, 1).replace(/"/g, "");
    console.debug(`Build options: ${stringify(buildOptions)}`);
    console.debug(`Build environment: ${stringify(environment)}`);
};
