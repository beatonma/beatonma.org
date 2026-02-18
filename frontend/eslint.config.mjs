import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.tsx", "**/*.t{s,sx}"],
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-unused-vars": "off",
      "@typescript-eslint/no-namespace": "off",
      "react/jsx-curly-brace-presence": "warn",
      "@next/next/no-img-element": "off",
    },
  },
]);
