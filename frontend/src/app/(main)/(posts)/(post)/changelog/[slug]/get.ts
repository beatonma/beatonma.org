import { type SlugParams, get } from "@/app/(main)/(posts)/(post)/util";

export const getChangelog = async (params: SlugParams) =>
  get("/api/changelog/{slug}/", params);
