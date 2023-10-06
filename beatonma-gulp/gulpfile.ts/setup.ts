import { sync as deleteSync } from "del";
import { ANY_FILE, distPath } from "./paths";
import { Env } from "./env";

export enum BuildMode {
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
export const getGitHash = () => environment.gitHash;

const init = async (_buildType: BuildMode) => {
    buildMode = _buildType;
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

const clean = () => deleteSync([distPath(ANY_FILE)]);
const checkConfiguration = () => {
    Object.entries(environment).forEach(([, value]) => {
        if (!value) {
            throw `Invalid environment: ${JSON.stringify(
                environment
            )} | ${JSON.stringify(process.env)}`;
        }
    });

    if (!buildMode) {
        throw `gulpfile task configuration error
            buildType must be set before calling 'build' task!
            Expected (${BuildMode.Development} | ${BuildMode.Production}),
            found '${buildMode}'\n`;
    } else {
        console.log(
            `Build configuration: ${buildMode} | ${JSON.stringify(environment)}`
        );
    }
};

export const initDev = async () => init(BuildMode.Development);
export const initTest = async () => init(BuildMode.Test);
export const initProduction = async () => init(BuildMode.Production);
