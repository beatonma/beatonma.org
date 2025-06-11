import { getOrNull } from "@/api";
import { PropsExcept } from "@/types/react";
import { GlobalHCard } from "./hcard";

export const AutoHCard = async (
  props: PropsExcept<typeof GlobalHCard, "hcard">,
) => {
  const state = await getOrNull("/api/state/");
  const hcard = state?.hcard;

  return <GlobalHCard hcard={hcard} {...props} />;
};
