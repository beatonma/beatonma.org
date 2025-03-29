"use client";

import { useCallback, useState } from "react";

/**
 * Returns a value and a function which triggers a change in that value.
 */
export const useFlag = (): [boolean, () => void] => {
  const [flag, setFlag] = useState(false);

  const toggle = useCallback(() => setFlag((prev) => !prev), []);

  return [flag, toggle];
};
