"use client";

import { useEffect, useState } from "react";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./bar.module.css";

export default function Bar(props: { progress?: number } & DivPropsNoChildren) {
  const { progress, ...rest } = props;

  if (progress == null) return <IndeterminateLoadingBar {...rest} />;
  return <ProgressLoadingBar progress={progress} {...rest} />;
}

const IndeterminateLoadingBar = (props: DivPropsNoChildren) => {
  const { ...rest } = addClass(props, styles.loadingBarIndeterminate);
  return <div {...rest} />;
};

const ProgressLoadingBar = (
  props: { progress: number } & DivPropsNoChildren,
) => {
  const { progress, ...rest } = addClass(props, styles.loadingBarDeterminate);
  const [isVisible, setVisible] = useState(true);

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout> | undefined;
    if (progress >= 100 && isVisible) {
      timeoutId = setTimeout(() => {
        setVisible(false);
      }, 3000);
    } else if (progress < 100 && !isVisible) {
      setVisible(true);
    }
    return () => clearTimeout(timeoutId);
  }, [isVisible, progress]);

  if (!isVisible) return null;

  return (
    <div {...rest}>
      <div
        className={styles.loadingBarDeterminateProgress}
        data-finished={progress >= 100}
        style={{ width: `${progress}%` }}
      />
    </div>
  );
};
