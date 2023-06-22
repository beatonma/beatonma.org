export type Url = string;

export type Repository = {
    id: number;
    name: string;
    description: string;
    url: Url;
    license?: string;
    payload: any;
};
