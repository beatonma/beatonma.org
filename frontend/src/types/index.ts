export type Nullish = null | undefined;

/**
 * Generate a tuple of type T with N values.
 */
export type TupleOf<
  T,
  N extends number,
  Acc extends T[] = [],
> = Acc["length"] extends N ? Acc : TupleOf<T, N, [...Acc, T]>;

/**
 * Make all properties of T optional and nullable.
 e.g:
* type A = {a: string, b: string}
* type B = Nullable<A>  // {a? string | Nullish, b?: string | Nullish}
*/
type Nullable<T> = {
  [P in keyof T]?: T[P] | Nullish;
};

/**
 * Make the properties of T from K nullable and optional.
 *
 * e.g:
 * type A = {a: string, b: string}
 * type B = Optional<A, "b">  // {a string, b?: string | Nullish}
 */
export type Optional<T, K extends keyof T> = Pick<Nullable<T>, K> &
  Omit<T, keyof Pick<T, K>>;
