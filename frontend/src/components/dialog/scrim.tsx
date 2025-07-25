import { useEffect, useState } from "react";
import { useKeyPress } from "@/components/hooks/inputs";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import styles from "./dialog.module.css";

interface ScrimProps {
  isVisible: boolean;
  scrimColor?: string;
  onClose: () => void;
}

export const Scrim = (props: DivProps<ScrimProps>) => {
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
};

export const ScrimBackground = (props: DivProps<ScrimProps>) => {
  const { isVisible, scrimColor, children, onClose, ...rest } = props;

  return (
    <div {...rest}>
      <Scrim isVisible={isVisible} scrimColor={scrimColor} onClose={onClose} />
      <div className="relative z-[110]">{children}</div>
    </div>
  );
};
