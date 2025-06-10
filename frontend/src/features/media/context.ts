"use client";

import { createContext } from "react";
import { OnClickMedia } from "./types";

export const OnClickMediaContext = createContext<OnClickMedia | undefined>(
  undefined,
);
