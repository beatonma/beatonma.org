import { type SlugParams, get } from "@/app/(main)/(posts)/(post)/util";

export const getApp = async (params: SlugParams) =>
  get("/api/apps/{slug}/", params);
