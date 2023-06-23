import { defineConfig } from "cypress";

export default defineConfig({
    chromeWebSecurity: false,
    e2e: {
        experimentalRunAllSpecs: true,
        supportFile: false,
    },
    trashAssetsBeforeRuns: false, // Keep screenshots
});
