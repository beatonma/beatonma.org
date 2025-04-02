"use client";

import React, { useEffect, useRef, useState } from "react";
import { Button } from "@/components/button";
import { onlyIf } from "@/util/optional";

export default function ReturnToTopButton() {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const checkVisibility = () => {
      const button = ref.current;
      if (!button) return;
      setIsVisible(!(button.offsetTop < window.innerHeight));
    };

    checkVisibility();
    window.addEventListener("resize", checkVisibility);
    return () => window.removeEventListener("resize", checkVisibility);
  }, []);

  return (
    <div ref={ref} className={onlyIf(!isVisible, "*:hidden size-[1px]")}>
      <Button href="#top" icon="ArrowUp">
        Return to top
      </Button>
    </div>
  );
}
