"use client";

import { ComponentProps, useEffect, useMemo, useRef, useState } from "react";
import { TextButton } from "@/components/button";
import { AppIcon } from "@/components/icon";

const StorageKey = "theme";
type Theme = "light" | "dark" | "system";
const ThemeController = (
  props: Omit<ComponentProps<"button">, "onClick" | "title">,
) => {
  const isInitialized = useRef<boolean>(false);
  const [mode, setMode] = useState<Theme>("system");
  const icon: AppIcon = useMemo(() => {
    switch (mode) {
      case "light":
        return "ThemeLightMode";
      case "dark":
        return "ThemeDarkMode";
      case "system":
      default:
        return "ThemeSystemDefault";
    }
  }, [mode]);

  useEffect(() => {
    if (!isInitialized.current) {
      setMode((localStorage.getItem(StorageKey) ?? "system") as Theme);
      isInitialized.current = true;
      return;
    }

    document.body.dataset.theme = mode;
    localStorage.setItem(StorageKey, mode);
  }, [mode]);

  return (
    <TextButton
      icon={icon}
      onClick={() => setMode(nextTheme(mode) ?? "system")}
      title={`Cycle theme (${mode})`}
      {...props}
    />
  );
};

const nextTheme = (theme: Theme) => {
  const themes: Theme[] = ["light", "dark", "system"];
  return themes[(themes.findIndex((it) => it === theme) + 1) % themes.length];
};

export default ThemeController;
