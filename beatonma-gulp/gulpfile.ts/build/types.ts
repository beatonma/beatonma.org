export interface Env {
    contactEmail: string;
    gitHash: string;
    googleRecaptchaToken: string;
    siteName: string;
}

export type StreamWrapper = (
    stream: NodeJS.ReadWriteStream,
) => NodeJS.ReadWriteStream;

export type BuildStream = (
    wrapper: StreamWrapper,
) => () => NodeJS.ReadWriteStream;

export type DjangoApp = string;
export type StaticResourceType = "js" | "css" | undefined | null;
