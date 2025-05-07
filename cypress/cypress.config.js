const defaultTimeout = 2_000;

module.exports = require("cypress").defineConfig({
  chromeWebSecurity: false, // Allow access to iframe elements (specifically: recaptcha)
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
  env: {
    NEXT_PUBLIC_SITE_NAME: process.env.NEXT_PUBLIC_SITE_NAME,
    NEXT_PUBLIC_GITHUB_USERNAME: process.env.NEXT_PUBLIC_GITHUB_USERNAME,
  },
});
