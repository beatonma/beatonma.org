import React, {
  ReactNode,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { Button } from "@/components/button";
import { useKeyPress } from "@/components/hooks/inputs";
import { AppIcon } from "@/components/icon";
import type { SelectorDivProps } from "@/components/selector/types";
import { DivProps } from "@/types/react";
import { onlyIf } from "@/util/optional";
import { addClass } from "@/util/transforms";

export const Select = (props: SelectorDivProps) => {
  const { selected, items, onSelect, ...rest } = props;

  return (
    <Popup
      anchor={selected.display}
      anchorIcon="ArrowDropDown"
      contents={(onClosePopup) => (
        <PopupMenuOptions
          selected={selected}
          items={items}
          onSelect={(it) => {
            onClosePopup();
            onSelect(it);
          }}
        />
      )}
      {...rest}
    />
  );
};

interface PopupProps {
  anchorIcon?: AppIcon;
  anchor: ReactNode;
  contents: (onClosePopup: () => void) => ReactNode;
}
const Popup = (
  props: DivProps<PopupProps, "children" | "onBlur" | "onSelect">,
) => {
  const [isExpanded, setExpanded] = useState(false);
  const { anchor, anchorIcon, contents, ...rest } = addClass(
    props,
    "relative select-none",
    onlyIf(isExpanded, "surface-alt"),
  );
  const ref = useRef<HTMLDivElement>(null);

  useKeyPress({
    Escape: () => setExpanded(false),
  });

  return (
    <div
      ref={ref}
      onBlur={(ev) => {
        if (ref.current && !ref.current.contains(ev.relatedTarget)) {
          setExpanded(false);
        }
      }}
      {...rest}
    >
      <Button
        icon={anchorIcon}
        onClick={() => setExpanded((prev) => !prev)}
        aria-haspopup="menu"
        aria-expanded={isExpanded}
      >
        {anchor}
      </Button>

      {onlyIf(
        isExpanded,
        contents(() => setExpanded(false)),
      )}
    </div>
  );
};

const PopupMenuOptions = (props: SelectorDivProps) => {
  const { selected, items, onSelect, ...rest } = addClass(
    props,
    "absolute right-0 min-w-full surface-alt shadow-md py-1 rounded-b-lg z-10",
  );
  const refs = useRef<(HTMLElement | null)[]>(Array(items.length));
  const focusIndex = useRef(items.indexOf(selected));

  const focus = useCallback(
    (index: number) => {
      const safeIndex =
        (index < 0 ? items.length + index : index) % items.length;
      focusIndex.current = safeIndex;
      refs.current[safeIndex]?.focus();
    },
    [items],
  );

  useKeyPress({
    ArrowDown: () => focus(focusIndex.current + 1),
    ArrowUp: () => focus(focusIndex.current - 1),
    " ": () => onSelect(items[focusIndex.current]),
    Enter: () => onSelect(items[focusIndex.current]),
  });

  useEffect(() => {
    focus(focusIndex.current);
  }, [focus]);

  return (
    <div {...rest}>
      <ul role="menu">
        {items.map((item, index) => (
          <li
            ref={(el) => {
              refs.current[index] = el;
            }}
            tabIndex={0}
            key={item.key}
            role="menuitem"
            onClick={() => onSelect(item)}
            className="hover-surface-alt select-none min-w-full px-2 py-1 whitespace-nowrap"
          >
            {item.display}
          </li>
        ))}
      </ul>
    </div>
  );
};
