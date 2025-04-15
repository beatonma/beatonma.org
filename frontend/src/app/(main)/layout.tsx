import React from "react";
import { getOrNull } from "@/api";
import MainLayout from "./_components/main-layout";

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const globalState = await getOrNull("/api/state/");
  return <MainLayout state={globalState}>{children}</MainLayout>;
}
