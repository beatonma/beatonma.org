import { useEffect, useState } from "react";
import styles from "@/components/dialog/dialog.module.css";
import useKeyPress from "@/components/hooks/key";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

interface ScrimProps {
  isVisible: boolean;
  scrimColor?: string;
  onClose: () => void;
}
export default function Scrim(props: ScrimProps & Omit<DivProps, "onClick">) {
  const { isVisible, scrimColor, onClose, ...rest } = addClass(
    props,
    styles.dialogScrim,
    props.scrimColor ?? "surface-scrim",
    "fixed inset-0 z-100",
  );
  const [hasBeenVisible, setHasBeenVisible] = useState(isVisible);

  useKeyPress({
    Escape: () => onClose(),
  });

  useEffect(() => {
    if (isVisible) {
      setHasBeenVisible(true);
    }
  }, [isVisible]);

  if (!hasBeenVisible) return null;
  return <div data-is-open={isVisible} onClick={onClose} {...rest} />;
}

export function ScrimBackground(props: ScrimProps & DivProps) {
  const { isVisible, scrimColor, children, onClose, ...rest } = props;

  return (
    <div {...rest}>
      <Scrim isVisible={isVisible} scrimColor={scrimColor} onClose={onClose} />
      <div className="relative z-[110]">{children}</div>
    </div>
  );
}
