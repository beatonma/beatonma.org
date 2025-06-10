import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./skeleton.module.css";

export const Skeleton = (props: DivProps) => (
  <div {...addClass(props, styles.skeleton)} />
);
