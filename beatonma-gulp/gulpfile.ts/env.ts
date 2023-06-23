import gulpReplace from "gulp-replace";
import { getEnvironment } from "./setup";


export interface Env {
    contactEmail: string;
    gitHash: string;
    googleRecaptchaToken: string;
    siteName: string;
}


/**
 * Inject __env__:key with value of env[key].
 */
export const includeEnv = () => {
    const env = getEnvironment();

    return gulpReplace(/__env__:(\w+)/g, function (match: string, key: string) {
        if (Object.keys(env).includes(key)) {
            console.debug(
                `__env__:${key} -> '${env[key as keyof Env]}' | ${
                    this.file.basename
                }`
            );
            return env[key as keyof Env] as string;
        } else {
            throw `Unknown environment key ${key}`;
        }
    });
};
