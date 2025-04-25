import { getOr404 } from "@/api";
import { PropsExcept } from "@/types/react";
import HCard from "./hcard";

export default async function AutoHCard(
  props: PropsExcept<typeof HCard, "hcard">,
) {
  const state = await getOr404("/api/state/");
  const hcard = state?.hcard;

  return <HCard hcard={hcard} {...props} />;
}
