"use client";

import Link from "next/link";
import { permanentRedirect, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { client } from "@/api";
import { LoadingSpinner } from "@/components/loading";
import { Prose } from "@/components/prose";
import { navigationHref } from "@/navigation";
import { Nullish } from "@/types";
import { MainLayout } from "./(main)/_components/main-layout";

export default function NotFound() {
  const path = usePathname();
  const [redirectTo, setRedirectTo] = useState<string | Nullish>(undefined);

  useEffect(() => {
    client
      .GET("/api/redirect/", {
        params: {
          query: {
            path,
          },
        },
      })
      .then((response) => {
        setRedirectTo(response.data?.redirect || null);
      })
      .catch((e) => {
        setRedirectTo(null);
      });
  }, [path]);

  if (redirectTo) return permanentRedirect(redirectTo);
  if (redirectTo === undefined)
    return (
      <MainLayout>
        <LoadingSpinner>
          <strong>Checking for redirects...</strong>
        </LoadingSpinner>
      </MainLayout>
    );

  return (
    <MainLayout>
      {/* Metadata not supported in not-found: https://github.com/vercel/next.js/issues/45620#issuecomment-1488933853 */}
      <title>404 not found</title>
      <Prose className="mx-auto">
        <h1>404 not found</h1>

        <p>
          Path <code>{path}</code> could not be resolved.
        </p>

        <p>
          If you followed a link to get here please{" "}
          <Link href={navigationHref("contact")}>let me know</Link> so I can fix
          it.
        </p>
      </Prose>
    </MainLayout>
  );
}
