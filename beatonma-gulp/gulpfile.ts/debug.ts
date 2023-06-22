import gulpRename from "gulp-rename";

export const printFilename = () =>
    gulpRename((path, file) => {
        console.log(file.path);
    });
