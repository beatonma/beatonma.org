This is the source for the frontend of [beatonma.org](https://beatonma.org).

The site uses a combination of static [Django](https://djangoproject.com) templates and dynamic [React](https://reactjs.org) components.

Source files are written with [Typescript](https://www.typescriptlang.org) and [Sass](https://sass-lang.com). [Gulp](https://gulpjs.com) is used to compile these to CSS and Javascript. It also applies transformations to template source files, making them easier to write.

Typescript and template files may include `__env__:key` to inject values at build time. This uses the `Env` interface defined [here](gulpfile.ts/build/types).
