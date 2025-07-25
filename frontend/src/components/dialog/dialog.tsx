"use client";

import {
  ComponentPropsWithoutRef,
  useCallback,
  useEffect,
  useRef,
} from "react";
import { createPortal } from "react-dom";
import { Button } from "@/components/button";
import { useClient } from "@/components/hooks/environment";
import { addClass } from "@/util/transforms";
import { Scrim } from "./scrim";

const DialogPortalContainerId = "dialog_portal_container";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Dialog = (
  props: DialogProps &
    Omit<ComponentPropsWithoutRef<"dialog">, keyof DialogProps | "onClick">,
) => {
  const { isOpen, onClose, children, ...rest } = props;
  const containerRef = useRef<HTMLDivElement | null>(null);
  const isClient = useClient();

  const keyboardController = useCallback(
    (ev: KeyboardEvent) => {
      if (ev.code === "Escape") {
        onClose();
        ev.preventDefault();
      }
    },
    [onClose],
  );

  useEffect(() => {
    if (isOpen) {
      window.addEventListener("keydown", keyboardController);
    }

    return () => window.removeEventListener("keydown", keyboardController);
  }, [isOpen, keyboardController]);

  useEffect(() => {
    containerRef.current = document.getElementById(
      DialogPortalContainerId,
    ) as HTMLDivElement;
  }, []);

  // Don't render anything until dialog has been requested.
  if (!isClient) return null;

  return createPortal(
    <Scrim
      isVisible={isOpen}
      onClose={onClose}
      className="flex justify-center items-center overflow-hidden"
    >
      {isOpen && (
        <dialog
          open={isOpen}
          onClick={(ev) => {
            ev.stopPropagation();
          }}
          {...addClass(
            rest,
            "[--max-width:95vw] [--max-height:95vh] max-h-(--max-height) max-w-(--max-width)",
            "surface-alt gap-4 overflow-hidden justify-self-center rounded-md",
            "grid grid-cols-1 grid-rows-[1fr_auto]",
          )}
        >
          <div className="overflow-hidden">{children}</div>
          <div className="p-4 justify-self-end w-fit">
            <Button
              icon="Close"
              onClick={(ev) => {
                ev.preventDefault();
                ev.stopPropagation();
                onClose();
              }}
              className="text-vibrant"
            >
              Close
            </Button>
          </div>
        </dialog>
      )}
    </Scrim>,
    containerRef.current!,
  );
};
