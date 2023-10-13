import { distPath } from "../paths";
import { Env } from "./types";
import { sync as deleteSync } from "del";

enum BuildMode {
    Development = "development",
    Production = "production",
    Test = "test",
}
let buildMode: BuildMode = null;
let environment: Env = null;

export const getWebpackBuildMode = (): "development" | "production" =>
    buildMode === BuildMode.Test ? BuildMode.Production : buildMode;

export const isDevBuild = (): boolean => buildMode === BuildMode.Development;
export const isProductionBuild = (): boolean =>
    buildMode === BuildMode.Production;
export const isTestBuild = (): boolean => buildMode === BuildMode.Test;

export const getEnvironment = () => environment;
export const injectGitHash = (filename: string): string =>
    filename.replace(
        /(?<basename>[^.]+)(?<extension>\.?.*)/,
        `$1-${environment.gitHash}$2`,
    );

export const initDev = async () => init(BuildMode.Development);
export const initTest = async () => init(BuildMode.Test);
export const initProduction = async () => init(BuildMode.Production);

const init = async (mode: BuildMode) => {
    buildMode = mode;
    environment = {
        gitHash: process.env.GIT_HASH ?? "__no_env__",
        contactEmail: process.env.WEBMAIL_CONTACT_EMAIL ?? "__no_env__",
        googleRecaptchaToken:
            process.env.GOOGLE_RECAPTCHA_TOKEN ?? "__no_env__",
        siteName: process.env.SITE_NAME ?? "__no_env__",
    };
    clean();
    checkConfiguration();
};

const clean = () => deleteSync([distPath("**")], { force: true });
const checkConfiguration = () => {
    if (!buildMode) {
        throw `gulpfile task configuration error
            buildType must be set before calling 'build' task!
            Expected (${BuildMode.Development} | ${BuildMode.Production}),
            found '${buildMode}'\n`;
    }
    console.info(
        `Build configuration: ${buildMode} | ${JSON.stringify(environment)}`,
    );
};
