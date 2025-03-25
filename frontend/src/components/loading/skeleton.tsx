import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./skeleton.module.css";

export default function Skeleton(props: DivProps) {
  return <div {...addClass(props, styles.skeleton)} />;
}
