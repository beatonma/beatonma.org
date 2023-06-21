export const ANY_HTML = "**/*.html";
export const ANY_FILE = "**";

/* Paths */
const SRC_PATH = "src/";
const DIST_PATH = "dist/";
// export const LOCAL_PATH = "../back/beatonma-django/";
const LOCAL_PATH = process.env.TEMPLATE_ROOT

export const srcPath = (path?: string) => joinPath(SRC_PATH, path);
export const distPath = (path?: string) => joinPath(DIST_PATH, path);

export const localPath = (path?: string) => joinPath(LOCAL_PATH, path);


const joinPath = (root: string, leaf: string | undefined) => {
    if (!leaf) return root;
    return `${root}${leaf}`;
};
