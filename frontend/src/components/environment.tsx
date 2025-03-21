import { useEffect, useState } from "react";
import { ChildrenProps } from "@/types/react";

export const useClient = () => {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return isMounted;
};

export const Client = (props: ChildrenProps) => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (isClient) return <>{props.children}</>;
};

export const Server = (props: ChildrenProps) => {
  if (typeof window === "undefined") return <>{props.children}</>;
};
