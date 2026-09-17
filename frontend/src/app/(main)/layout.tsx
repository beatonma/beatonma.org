import { ReactNode } from "react";
import Repository from "@/repository";
import { MainLayout } from "./_components/main-layout";

export const dynamic = "force-dynamic";

export default async function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  const globalState = await Repository.getGlobalState();

  return <MainLayout state={globalState}>{children}</MainLayout>;
}
