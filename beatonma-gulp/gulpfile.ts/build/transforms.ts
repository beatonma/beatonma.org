import { Transform } from "node:stream";
import Vinyl from "vinyl";

export const ignore =
    (condition: (file: Vinyl) => boolean) => (): NodeJS.ReadWriteStream =>
        new Transform({
            objectMode: true,
            transform(
                file: Vinyl,
                encoding: BufferEncoding,
                callback: (error?: Error | null, data?: any) => void,
            ) {
                if (condition(file)) {
                    console.debug(`ignore ${file.relative}`);
                    return callback();
                }
                return callback(null, file);
            },
        });
