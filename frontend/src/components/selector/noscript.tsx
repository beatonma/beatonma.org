import { ReactNode } from "react";
import { InlineLink } from "@/components/button";
import { Client } from "@/components/hooks/environment";
import { Row } from "@/components/layout";
import type { SelectorDivProps } from "@/components/selector/types";

const NoscriptSelect = (props: SelectorDivProps) => {
  const { selected, items, onSelect, ...rest } = props;

  return (
    <noscript {...rest}>
      <Row scrollable className="gap-2">
        {items.map((it) => (
          <InlineLink
            key={it.key}
            href={it.href}
            icon={null}
            className={
              selected.key === it.key
                ? "decoration-vibrant decoration-2 underline font-medium"
                : "opacity-80"
            }
          >
            {it.display}
          </InlineLink>
        ))}
      </Row>
    </noscript>
  );
};

export const NoscriptSelectWrapper = (
  props: SelectorDivProps & {
    reactNode: () => ReactNode;
  },
) => {
  const { reactNode, ...rest } = props;

  return (
    <>
      <NoscriptSelect {...rest} />
      <Client>{reactNode()}</Client>
    </>
  );
};
