const IntFormat = new Intl.NumberFormat("en-GB", { maximumFractionDigits: 0 });
const FloatFormat = new Intl.NumberFormat("en-GB", {
  maximumFractionDigits: 2,
});

export const percentage = (value: number) => value.toFixed(0);
export const int = (value: number) => IntFormat.format(value);
export const float = (value: number) => FloatFormat.format(value);
