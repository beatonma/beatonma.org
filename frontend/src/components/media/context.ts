"use client";

import { createContext } from "react";
import { OnClickMedia } from "@/components/media/types";

export const OnClickMediaContext = createContext<OnClickMedia | undefined>(
  undefined,
);
