module.exports = async () => ({
    modulePathIgnorePatterns: [
        "build/",
        "dist/",
        "env/",
        "node_modules/",
        "tools/",
        "cypress/",
    ],
    testEnvironment: "jsdom",
});
