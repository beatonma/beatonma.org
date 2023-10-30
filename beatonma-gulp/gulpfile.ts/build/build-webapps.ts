import { srcPath } from "../paths";
import { isProductionBuild } from "./config";
import { shell_command } from "./util";
import * as glob from "glob";
import path from "path";

const Webapps = srcPath("webapp/*/package.json");

const npmInstall = (cwd: string) => shell_command("npm install", cwd);
const npmBuild = (cwd: string) => shell_command("npm run build", cwd);

export const buildWebapps = (mapToOutput: (webappDir: string) => void) =>
    function buildWebapps() {
        return new Promise<void>((resolve, reject) => {
            const webappGlobs = glob.sync(Webapps);
            const builders = webappGlobs.map(async filepath => {
                const webappCwd = path.dirname(filepath);
                if (isProductionBuild()) {
                    await npmInstall(webappCwd);
                }
                await npmBuild(webappCwd);
                return mapToOutput(webappCwd);
            });
            Promise.all(builders).then(() => resolve());
        });
    };
