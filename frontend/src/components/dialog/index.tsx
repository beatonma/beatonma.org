import { ComponentPropsWithoutRef, useCallback, useEffect } from "react";
import { Button } from "@/components/button";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import "./dialog.css";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
}
export default function Dialog(
  props: DialogProps &
    Omit<ComponentPropsWithoutRef<"dialog">, keyof DialogProps | "onClick">,
) {
  const { isOpen, onClose, children, ...rest } = props;

  const keyboardController = useCallback((ev: KeyboardEvent) => {
    if (ev.code === "Escape") {
      onClose();
      ev.preventDefault();
    }
  }, []);

  useEffect(() => {
    if (isOpen) {
      window.addEventListener("keydown", keyboardController);
    }

    return () => window.removeEventListener("keydown", keyboardController);
  }, [isOpen]);

  return (
    <>
      <Scrim
        data-is-open={isOpen}
        onClick={() => onClose()}
        className="flex justify-center items-center overflow-hidden"
      >
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
              onClick={() => onClose()}
              className="text-vibrant"
            >
              Close
            </Button>
          </div>
        </dialog>
      </Scrim>
    </>
  );
}

const Scrim = (props: DivProps) => {
  const { ...rest } = addClass(
    props,
    "dialog-scrim",
    "fixed inset-0 surface-scrim z-100",
  );

  return <div {...rest} />;
};
