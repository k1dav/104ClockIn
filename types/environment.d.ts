export {};

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      account: string;
      password: string;
      gmail_token: string;
    }
  }
}
