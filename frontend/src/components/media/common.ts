"use client";

import { createContext } from "react";
import { schemas } from "@/api";

export type MediaFile = schemas["File"];
export type OnClickMedia = (media: MediaFile) => void;
export const OnClickMediaContext = createContext<OnClickMedia | undefined>(
  undefined,
);
