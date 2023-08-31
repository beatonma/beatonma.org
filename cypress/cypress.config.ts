import { defineConfig } from "cypress";

const defaultTimeout = 2_000;

export default defineConfig({
  chromeWebSecurity: false,
  e2e: {
    experimentalRunAllSpecs: true,
    supportFile: false,
  },
  trashAssetsBeforeRuns: false, // Keep screenshots,
  defaultCommandTimeout: defaultTimeout,
  taskTimeout: 10_000,
  execTimeout: 5_000,
  pageLoadTimeout: defaultTimeout,
  requestTimeout: defaultTimeout,
  responseTimeout: defaultTimeout,
});
