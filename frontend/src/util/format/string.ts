import { Nullish } from "@/types";

export const capitalize = (value: string | Nullish): string | null =>
  value ? value.slice(0, 1).toUpperCase() + value.slice(1) : null;
