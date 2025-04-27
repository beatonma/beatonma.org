"use client";

import { useEffect, useState } from "react";
import { Props } from "@/types/react";

type Dimension = number | undefined;
export default function LocalIFrame(props: Props<"iframe">) {
  const [size, setSize] = useState<[Dimension, Dimension]>([
    undefined,
    undefined,
  ]);
  const [width, height] = size;

  useEffect(() => {
    const handler = (ev: MessageEvent) => {
      try {
        const { width, height } = ev.data;

        setSize([width, height]);
      } catch (e) {
        console.error(`IFrame message error: ${e}`);
      }
    };

    addEventListener("message", handler);
    return () => {
      removeEventListener("message", handler);
    };
  }, []);

  return <iframe width={width} height={height} {...props} />;
}
