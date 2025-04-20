import React from "react";
import { getOrNull } from "@/api";
import MainLayout from "./_components/main-layout";

export const dynamic = "force-dynamic";

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const globalState = await getOrNull("/api/state/");
  return <MainLayout state={globalState}>{children}</MainLayout>;
}
