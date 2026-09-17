const config = {
  input: "http://localhost:8000/api/openapi.json",
  output: "frontend/src/api/client",
  plugins: [
    {
      name: "@hey-api/client-next",
      runtimeConfigPath: "@/api/hey-api",
    },
  ],
};
export default config;
