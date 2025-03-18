export const onlyIf = <T, R>(
  value: T | null | undefined,
  block?: R | ((value: T) => R),
): R | undefined => {
  if (isTruthy(value)) {
    if (block == null) return value as any as R;
    return isFunction(block) ? block(value) : block;
  }
};

const isTruthy = <T>(
  value: T | null | undefined,
  condition?: (value: T) => boolean,
): value is T => {
  if (value == null) return false;
  if (condition) return condition(value);
  if (value === false) return false;
  if (typeof value === "string") return !!value;
  if (Array.isArray(value) && value.length === 0) return false;

  return true;
};
const isFunction = <T, R>(
  value: R | ((value: T) => R),
): value is (value: T) => R => {
  return typeof value === "function";
};
