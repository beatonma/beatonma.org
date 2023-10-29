const path = require("path");

module.exports = (env: any) => {
    const isProduction = env.production;
    return {
        mode: isProduction ? "production" : "development",
        devtool: isProduction ? "source-map" : "eval",
        devServer: {
            port: 3005,
            static: "./",
        },
        optimization: {
            minimize: isProduction,
        },
        entry: "./entrypoint.tsx",
        output: {
            filename: "palette.js",
            path: path.resolve(__dirname, "dist"),
        },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /node_modules/,
                    use: "swc-loader",
                },
                {
                    test: /\.scss$/,
                    use: ["style-loader", "css-loader", "sass-loader"],
                },
            ],
        },
        resolve: {
            extensions: [".js", ".ts", ".tsx"],
        },
    };
};
