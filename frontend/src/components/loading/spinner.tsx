import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./spinner.module.css";

export default function Spinner(props: DivPropsNoChildren) {
  return (
    <div {...addClass(props, styles.spinner)}>
      <div className={styles.spinnerWrapper}>
        <div className={styles.spinnerChild} />
        <div className={styles.spinnerChild} />
        <div className={styles.spinnerChild} />
      </div>
      <noscript className="text-sm">
        Loading error: javascript is disabled.
      </noscript>
    </div>
  );
}
