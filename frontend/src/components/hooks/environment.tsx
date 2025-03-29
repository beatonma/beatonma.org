import { useEffect, useState } from "react";
import { ChildrenProps } from "@/types/react";

/**
 * If return value is true then we are in a javascript-enabled client environment.
 * Otherwise, server or
 */
export const useClient = () => {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return isMounted;
};

export const Client = (props: ChildrenProps) => {
  const isClient = useClient();

  if (isClient) return <>{props.children}</>;
};
