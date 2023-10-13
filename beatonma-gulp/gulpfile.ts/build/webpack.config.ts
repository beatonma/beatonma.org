import { Configuration } from "webpack";

type BuildMode = "development" | "production";
/**
 * This is called from gulp - not a valid standalone webpack configuration file.
 */
export const getConfig: (mode: BuildMode) => Configuration = (
    mode: BuildMode,
) => {
    const isProduction = mode === "production";

    return {
        mode: mode,
        devtool: isProduction ? "source-map" : "inline-source-map",
        optimization: {
            minimize: isProduction,
        },
        output: {
            filename: "[name].js",
        },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: "swc-loader",
                    },
                },
            ],
        },
        resolve: {
            extensions: [".ts", ".tsx"],
        },
    };
};
