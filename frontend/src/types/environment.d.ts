declare global {
  namespace NodeJS {
    interface ProcessEnv {
      API_BASE_URL: string | undefined;
      NEXT_PUBLIC_SITE_NAME: string;
      NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION: string;
      NEXT_PUBLIC_GOOGLE_RECAPTCHA_TOKEN: string;
      NEXT_PUBLIC_GITHUB_USERNAME: string;
    }
  }
}

export {};
