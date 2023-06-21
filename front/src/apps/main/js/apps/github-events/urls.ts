import { Repository } from "./types/common";

export namespace GithubUrl {
    export const tag = (repo: Repository, tag: string) =>
        `${repo.url}/releases/tag/${tag}`;

    export const tags = (repo: Repository) => `${repo.url}/tags`;

    export const branches = (repo: Repository) => `${repo.url}/branches`;

    export const wiki = (repo: Repository) => `${repo.url}/wiki`;
}
