import { type SlugParams, get } from "@/app/(main)/(posts)/(post)/util";

export const getPost = async (params: SlugParams) => get("/api/posts/{slug}/", params)
