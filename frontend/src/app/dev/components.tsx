"use client";

import { ComponentPropsWithoutRef } from "react";
import { TextButton, TintedButton } from "@/components/button";
import Icon, { _private as Icon_private } from "@/components/icon";
import { Row } from "@/components/layout";
import Loading, { LoadingBar } from "@/components/loading";
import { addClass } from "@/util/transforms";

const Section = (props: ComponentPropsWithoutRef<"section">) => (
  <section {...addClass(props, " gap-4 items-start")} />
);

export const Buttons = () => (
  <Section>
    <Row className="gap-4">
      <TextButton href="#">TextButton</TextButton>
      <TintedButton href="#">TintedButton</TintedButton>
    </Row>
  </Section>
);
export const Icons = () => {
  const icons = Icon_private.Icons;

  return (
    <Section>
      <div className="card card-content surface grid grid-cols-[repeat(auto-fit,96px)] gap-2">
        {icons.map((icon) => (
          <div
            key={icon}
            className="relative aspect-square text-[96px] border-1 border-dashed border-current"
          >
            <div className="absolute inset-0 m-[8px] border-dashed border-1 border-vibrant" />
            <Icon icon={icon} />
          </div>
        ))}
      </div>
    </Section>
  );
};

export const Loaders = () => (
  <Section>
    <Loading />
    <LoadingBar />
  </Section>
);
