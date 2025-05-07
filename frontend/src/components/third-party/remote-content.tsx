"use client";

import { ReactNode, useEffect, useState } from "react";
import { Button } from "@/components/button";
import { Row } from "@/components/layout";
import Loading from "@/components/loading";
import Prose from "@/components/prose";
import { DivPropsNoChildren } from "@/types/react";
import { testId } from "@/util";

const TestTarget = {
  AllowRemoteContent: "allow_remote_content",
};

export interface RemoteContentProvider {
  domain: string;
  description: ReactNode;
}

interface RemoteContentProps {
  provider: RemoteContentProvider;
  content: () => ReactNode;
}
export default function RemoteContent(
  props: RemoteContentProps &
    Omit<DivPropsNoChildren, keyof RemoteContentProps>,
) {
  const { provider, content, ...rest } = props;
  const [isAllowed, setIsAllowed] = useState<boolean>();

  useEffect(() => {
    if (isAllowed === undefined) {
      setIsAllowed(getSavedPreference(provider));
      return;
    }

    setSavedPreference(provider, isAllowed);
  }, [provider, isAllowed]);

  if (isAllowed === undefined) return <Loading />;
  if (isAllowed) return <>{content()}</>;

  return (
    <Prose {...rest}>
      <h3>
        Allow content from{" "}
        <span className="text-vibrant">{provider.domain}</span>?
      </h3>
      <p>{provider.description}</p>

      <Row className="justify-end">
        <Button
          className="text-vibrant self-end"
          onClick={() => setIsAllowed(true)}
          {...testId(TestTarget.AllowRemoteContent)}
        >
          Allow
        </Button>
      </Row>
    </Prose>
  );
}

const storageKeyOf = (provider: RemoteContentProvider) =>
  `remotecontentprovider__${provider.domain}`;

const getSavedPreference = (provider: RemoteContentProvider): boolean =>
  window.localStorage.getItem(storageKeyOf(provider))?.toLowerCase() === "true";

const setSavedPreference = (
  provider: RemoteContentProvider,
  allow: boolean,
) => {
  window.localStorage.setItem(storageKeyOf(provider), `${allow}`);
};
