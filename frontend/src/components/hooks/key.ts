import { useEffect } from "react";

type Modifier = "control" | "shift" | "alt" | "meta";
type OnKeyPress = Record<
  string,
  (modifiers: Record<Modifier, boolean>) => void
>;

export default function useKeyPress(actions: OnKeyPress) {
  useEffect(() => {
    const onKeyDown = (ev: KeyboardEvent) => {
      const action = actions[ev.key];
      if (action) {
        action({
          shift: ev.shiftKey,
          control: ev.ctrlKey,
          alt: ev.altKey,
          meta: ev.metaKey,
        });
        ev.preventDefault();
        ev.stopPropagation();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [actions]);
}
