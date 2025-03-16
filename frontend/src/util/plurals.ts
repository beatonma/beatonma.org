import { int } from "@/components/number";

/**
 * [Single: ZeroOrMany]
 */
const Plurals = {
  result: ["result", "results"],
};

export const plural = (key: keyof typeof Plurals, count: number) => {
  const index = count === 1 ? 0 : 1;

  return `${int(count)} ${Plurals[key][index]}`;
};
