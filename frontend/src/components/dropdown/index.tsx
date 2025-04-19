import { ReactNode } from "react";
import { Props } from "@/types/react";

interface DropdownProps {
  summary: ReactNode;
}
export default function Dropdown(props: DropdownProps & Props<"details">) {
  const { summary, children, ...rest } = props;
  return (
    <details {...rest}>
      <summary className="cursor-default">{summary}</summary>

      {children}
    </details>
  );
}
