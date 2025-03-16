import { ComponentPropsWithoutRef } from "react";

const NumberFormat = new Intl.NumberFormat("en-GB");

export const percentage = (value: number) => value.toFixed(0);
export const int = (value: number) => NumberFormat.format(value);

export const Percentage = (
  props: { value: number } & ComponentPropsWithoutRef<"span">,
) => {
  const { value, ...rest } = props;
  return (
    <span {...rest}>
      {percentage(value)}
      <span className="opacity-70">%</span>
    </span>
  );
};
