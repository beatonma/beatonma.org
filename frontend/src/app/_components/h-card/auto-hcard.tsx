import Repository from "@/repository";
import { PropsExcept } from "@/types/react";
import { GlobalHCard } from "./hcard";

export const AutoHCard = async (
  props: PropsExcept<typeof GlobalHCard, "hcard">,
) => {
  const state = await Repository.getGlobalState();
  const hcard = state?.hcard;

  return <GlobalHCard hcard={hcard} {...props} />;
};
