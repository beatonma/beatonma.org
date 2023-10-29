import child_process from "child_process";

export const shell_command = (command: string, cwd: string = ".") =>
    new Promise<void>((resolve, reject) => {
        child_process.exec(
            command,
            { cwd: cwd, timeout: 90_000 },
            (error, stdout, stderr) => {
                if (error) {
                    console.error(`${command}: ${error}`);
                    if (stderr) console.error(stderr);
                    if (stdout) console.error(stdout);
                    return reject(error);
                }
                resolve();
            },
        );
    });
