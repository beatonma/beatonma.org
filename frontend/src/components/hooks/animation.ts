import { useEffect, useState } from "react";
import styles from "./animation.module.css";

/**
 * Returns a different (but equivalent) fade-in animation class each time
 * a `flag` changes, triggering the animation to start anew.
 */
export const useFadeIn = (flag: any) => {
  const [anim, setAnim] = useState(styles.fadeIn_a);

  useEffect(() => {
    setAnim((prev) => {
      return {
        [styles.fadeIn_a]: styles.fadeIn_b,
        [styles.fadeIn_b]: styles.fadeIn_a,
      }[prev];
    });
  }, [flag]);

  return anim;
};
