import { CSSProperties } from "react";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

interface RemoteIconProps {
  src: string;
  mask?: boolean;
}
export const RemoteIcon = (props: DivPropsNoChildren<RemoteIconProps>) => {
  const { src, mask = true, style, ...rest } = addClass(props, "size-em");

  const maskStyle: CSSProperties = mask
    ? {
        backgroundColor: "currentColor",
        maskImage: `url('${src}')`,
        maskSize: "1em",
      }
    : {
        backgroundImage: `url('${src}')`,
        backgroundSize: "1em",
      };

  return <div style={{ ...style, ...maskStyle }} {...rest} />;
};
