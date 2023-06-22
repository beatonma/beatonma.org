export const classes = (...names: (string | undefined)[]) =>
    names.filter(it => !!it).join(" ");
