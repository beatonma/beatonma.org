export type Nullish = null | undefined;
export type Maybe<T> = T | undefined;
export type MaybeString = Maybe<string>;

/**
 * Generate a tuple of type T with N values.
 */
export type TupleOf<
  T,
  N extends number,
  Acc extends T[] = [],
> = Acc["length"] extends N ? Acc : TupleOf<T, N, [...Acc, T]>;
