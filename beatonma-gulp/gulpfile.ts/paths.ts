export const ANY_HTML = "**/*.html";
export const ANY_FILE = "**";

/* Paths */
const SRC_PATH = "src/";
const DIST_PATH = "dist/";
const LOCAL_PATH = process.env.GULP_OUTPUT_ROOT;
const DJANGO_PATH = process.env.DJANGO_ROOT;

export const srcPath = (path?: string) => joinPath(SRC_PATH, path);
export const distPath = (path?: string) => joinPath(DIST_PATH, path);

export const localPath = (path?: string) => joinPath(LOCAL_PATH, path);
export const djangoPath = (path?: string) => joinPath(DJANGO_PATH, path);

const joinPath = (root: string, leaf: string | undefined) => {
    if (!leaf) return root;
    return `${root}${leaf}`;
};
