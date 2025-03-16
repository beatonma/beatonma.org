import Icon from "@/components/icon";
import { DivPropsNoChildren } from "@/types/react";
import "./loading.css";

export { LoadingBar } from "./loading-bar";

export default function Loading(props: DivPropsNoChildren) {
  return (
    <div className="loading" {...props}>
      <Icon icon="MB" />
    </div>
  );
}
