import del from "del";
import { ANY_FILE, distPath } from "./paths";
import { Env} from "./env";

enum BuildMode {
    Development = "development",
    Production = "production",
}
let buildMode: BuildMode = null;
let environment: Env = null;

export const getBuildMode = () => buildMode;
export const isDevBuild = () => buildMode === BuildMode.Production;
export const isProductionBuild = () => buildMode === BuildMode.Development;

export const getEnvironment = () => environment;
export const getGitHash = () => environment.gitHash;


const clean = async () => del.sync([distPath(ANY_FILE)]);

const init = async (_buildType: BuildMode) => {
    buildMode = _buildType;
    environment = {
        gitHash: process.env.GIT_HASH,
        contactEmail: process.env.WEBMAIL_CONTACT_EMAIL,
        googleRecaptchaToken: process.env.GOOGLE_RECAPTCHA_TOKEN,
        siteName: process.env.SITE_NAME,
    };
    await clean()
}
export const initDev = async () =>  init(BuildMode.Development);
export const initProduction = async () => init(BuildMode.Production);

export const checkConfiguration = async () => {
    Object.entries(environment).forEach(([, value]) => {
        if (!value) {
            throw `Invalid environment: ${JSON.stringify(environment)} | ${JSON.stringify(process.env)}`;
        }
    })

    if (!buildMode) {
        throw `gulpfile task configuration error
            buildType must be set before calling 'build' task!
            Expected (${BuildMode.Development} | ${BuildMode.Production}),
            found '${buildMode}'\n`;
    } else {
        console.log(`Build configuration: ${buildMode} | ${JSON.stringify(environment)}`);
    }
};
