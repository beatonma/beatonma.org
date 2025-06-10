import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./spinner.module.css";

export const LoadingSpinner = (props: DivProps) => {
  const { children, ...rest } = props;
  return (
    <div {...addClass(rest, styles.spinner)}>
      <div className={styles.spinnerWrapper}>
        <div className={styles.spinnerChild} />
        <div className={styles.spinnerChild} />
        <div className={styles.spinnerChild} />
      </div>
      {children}
      <noscript className="text-sm">
        Loading error: javascript is disabled.
      </noscript>
    </div>
  );
};
