import { ComponentPropsWithoutRef } from "react";
import { TintedButton } from "@/components/button";
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

  return (
    <>
      <Scrim data-is-open={isOpen} onClick={() => onClose()}>
        <dialog
          open={isOpen}
          {...addClass(
            rest,
            "bg-transparent column items-center max-h-[95vh] gap-4",
          )}
        >
          {children}
          <TintedButton icon="Close" onClick={() => onClose()} className="m-4">
            Close
          </TintedButton>
        </dialog>
      </Scrim>
    </>
  );
}

const Scrim = (props: DivProps) => {
  const { ...rest } = addClass(
    props,
    "dialog-scrim",
    "fixed inset-0 bg-scrim z-100 flex justify-center items-center",
  );

  return <div {...rest} />;
};
