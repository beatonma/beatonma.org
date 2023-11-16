import child_process from "child_process";

export const shell_command = (command: string, cwd: string = ".") =>
    new Promise<void>((resolve, reject) => {
        console.info(`> ${command} [${cwd}]`);
        child_process.exec(
            command,
            { cwd: cwd, timeout: 90_000 },
            (error, stdout, stderr) => {
                if (stdout) console.debug(stdout);
                if (error) {
                    console.error(`${command}: ${error}`);
                    if (stderr) console.error(stderr);
                    return reject(error);
                }
                resolve();
            },
        );
    });
