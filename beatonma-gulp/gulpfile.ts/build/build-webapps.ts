import { srcPath } from "../paths";
import child_process from "child_process";
import * as glob from "glob";
import path from "path";

const Webapps = srcPath("webapp/*/package.json");

const npmBuild = (cwd: string) =>
    new Promise<void>((resolve, reject) => {
        child_process.exec(
            "npm run build",
            { cwd: cwd, timeout: 60_000 },
            (error, stdout, stderr) => {
                if (error) {
                    console.error(`NPM build error: ${error}`);
                    if (stderr) console.error(stderr);
                    if (stdout) console.error(stdout);
                    return reject(error);
                }
                resolve();
            },
        );
    });

export const buildWebapps = (mapToOutput: (webappDir: string) => void) =>
    function buildWebapps() {
        return new Promise<void>((resolve, reject) => {
            const webappGlobs = glob.sync(Webapps);
            const builders = webappGlobs.map(async filepath => {
                const webappCwd = path.dirname(filepath);
                await npmBuild(webappCwd);
                return mapToOutput(webappCwd);
            });
            Promise.all(builders).then(() => resolve());
        });
    };
