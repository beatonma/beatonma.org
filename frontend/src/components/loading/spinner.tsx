import Icon from "@/components/icon";
import { DivPropsNoChildren } from "@/types/react";
import styles from "./spinner.module.css";

export default function Spinner(props: DivPropsNoChildren) {
  return (
    <div className={styles.loading} {...props}>
      <Icon icon="MB" className={styles.loadingChild} />
    </div>
  );
}
