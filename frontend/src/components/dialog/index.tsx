"use client";

import {
  ComponentPropsWithoutRef,
  MouseEvent,
  useCallback,
  useEffect,
  useRef,
} from "react";
import { createPortal } from "react-dom";
import { Button } from "@/components/button";
import { useClient } from "@/components/environment";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./dialog.module.css";

const DialogPortalContainerId = "dialog_portal_container";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Dialog(
  props: DialogProps &
    Omit<ComponentPropsWithoutRef<"dialog">, keyof DialogProps | "onClick">,
) {
  const { isOpen, onClose, children, ...rest } = props;
  const containerRef = useRef<HTMLDivElement | null>(null);
  const isMounted = useClient();

  useEffect(() => {
    if (isOpen) {
      window.addEventListener("keydown", keyboardController);
    }

    return () => window.removeEventListener("keydown", keyboardController);
  }, [isOpen]);

  useEffect(() => {
    containerRef.current = document.getElementById(
      DialogPortalContainerId,
    ) as HTMLDivElement;
  }, []);

  const keyboardController = useCallback((ev: KeyboardEvent) => {
    if (ev.code === "Escape") {
      onClose();
      ev.preventDefault();
    }
  }, []);
  const onClickClose = useCallback(
    (ev: MouseEvent) => {
      ev.preventDefault();
      ev.stopPropagation();
      onClose();
    },
    [onClose],
  );

  if (!isMounted) return null;
  return createPortal(
    <Scrim
      data-is-open={isOpen}
      onClick={onClickClose}
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
            "surface-alt column gap-4 overflow-hidden justify-self-center rounded-md",
          )}
        >
          {children}
          <div className="p-4 self-end w-fit">
            <Button
              icon="Close"
              onClick={onClickClose}
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
}

const Scrim = (props: DivProps) => {
  const { ...rest } = addClass(
    props,
    styles.dialogScrim,
    "fixed inset-0 surface-scrim z-100",
  );

  return <div {...rest} />;
};
