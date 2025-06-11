"use client";

import Script from "next/script";
import { useCallback, useEffect, useId, useRef, useState } from "react";
import { LoadingSkeleton } from "@/components/loading";
import { testId } from "@/util";

const TestTarget = {
  RecaptchaWrapper: "recaptcha_wrapper",
};

declare global {
  interface Window {
    grecaptcha?: {
      render?: (
        containerId: string,
        params: GRecaptchaRenderParameters,
      ) => void;
    };
  }
}

interface GRecaptchaRenderParameters {
  sitekey: string;
  theme: "dark" | "light";
  size: "compact" | "normal";
  tabindex: number;
  callback: (token: string) => void;
  "expired-callback": () => void;
  "error-callback": () => void;
}

export interface RecaptchaProps {
  recaptchaPublicSiteKey: string;
}

interface RecaptchaCallbacks {
  onSuccess: (token: string) => void;
  onExpired: () => void;
  onError: () => void;
}

export const Recaptcha = (props: RecaptchaProps & RecaptchaCallbacks) => {
  const { recaptchaPublicSiteKey, onSuccess, onError, onExpired } = props;
  const [isLoaded, setIsLoaded] = useState(false);
  const containerId = useId();
  const isRendered = useRef(false);

  const onLoad = useCallback(() => {
    if (!window.grecaptcha?.render)
      throw new Error("onLoad should not be called before grecaptcha loads.");

    if (isRendered.current) return;
    isRendered.current = true;
    window.grecaptcha.render(containerId, {
      sitekey: recaptchaPublicSiteKey,
      size: "normal",
      theme: "light",
      tabindex: 0,
      callback: onSuccess,
      "error-callback": onError,
      "expired-callback": onExpired,
    });
  }, [containerId, recaptchaPublicSiteKey, onSuccess, onError, onExpired]);

  useEffect(() => {
    if (isLoaded) {
      onLoad();
      return;
    }

    const intervalId: ReturnType<typeof setInterval> = setInterval(() => {
      if (typeof window !== "undefined" && window.grecaptcha?.render) {
        setIsLoaded(true);
      }
    }, 200);

    return () => {
      clearInterval(intervalId);
    };
  }, [onLoad, isLoaded]);

  const RecaptchaRenderedSize = "min-w-[304px] min-h-[78px]";
  return (
    <div
      className={RecaptchaRenderedSize}
      {...testId(TestTarget.RecaptchaWrapper)}
    >
      {!isLoaded && <LoadingSkeleton className={RecaptchaRenderedSize} />}
      <div id={containerId} />
      <Script
        src="https://recaptcha.net/recaptcha/api.js?render=explicit"
        async
        defer
      />
    </div>
  );
};
