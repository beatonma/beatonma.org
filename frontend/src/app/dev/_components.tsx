"use client";

import { ComponentPropsWithoutRef } from "react";
import {
  Button,
  InlineButton,
  InlineLink,
  TintedButton,
} from "@/components/button";
import Callout from "@/components/callout";
import Icon, { _private as Icon_private } from "@/components/icon";
import { Row } from "@/components/layout";
import Loading, { LoadingBar, LoadingSkeleton } from "@/components/loading";
import { addClass } from "@/util/transforms";

const Section = (
  props: { name?: string } & ComponentPropsWithoutRef<"section">,
) => {
  const { name, children, ...rest } = addClass(props, "last:mb-32");
  return (
    <section {...rest}>
      {name && <h2>{name}</h2>}
      {children}
    </section>
  );
};

export const Buttons = () => (
  <Section name="Buttons" className="space-y-2">
    <Row className="gap-4 flex-wrap">
      <InlineButton icon="MB" href="#" />
      <InlineButton href="#">InlineButton</InlineButton>
      <InlineButton onClick={() => console.log("click")} icon="MB">
        InlineButton
      </InlineButton>
      <InlineButton disabled onClick={() => console.log("click")} icon="MB">
        disabled
      </InlineButton>
    </Row>

    <Row className="gap-4 flex-wrap">
      <TintedButton icon="MB" href="#" />
      <TintedButton href="#">TintedButton</TintedButton>
      <TintedButton onClick={() => console.log("click")} icon="MB">
        TintedButton
      </TintedButton>
      <TintedButton disabled onClick={() => console.log("click")} icon="MB">
        disabled
      </TintedButton>
    </Row>

    <Row className="gap-4 flex-wrap">
      <Button icon="MB" href="#" />
      <Button href="#">Button</Button>
      <Button onClick={() => console.log("click")} icon="MB">
        Button
      </Button>
      <Button disabled onClick={() => console.log("click")} icon="MB">
        disabled
      </Button>
    </Row>

    <Row className="gap-4 flex-wrap">
      <InlineLink icon="MB" href="https://beatonma.org" />
      <InlineLink href="https://beatonma.org" />
    </Row>
  </Section>
);
export const Icons = () => {
  const icons = Icon_private.Icons;

  return (
    <Section name="Icons">
      <div className=" grid grid-cols-[repeat(auto-fit,96px)] gap-2">
        {icons.map((icon) => (
          <div key={icon} title={icon}>
            <div className="relative aspect-square text-[96px] border-1 border-dashed border-current">
              <div className="absolute inset-0 m-[8px] border-dashed border-1 border-vibrant" />
              <Icon icon={icon} />
            </div>
            <div className="text-xs font-mono overflow-ellipsis w-full overflow-hidden text-center p-1">
              {icon}
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
};

export const Loaders = () => (
  <Section name="Loading" className="space-y-2">
    <Loading />
    <LoadingBar />
    <LoadingBar progress={64} />
    <LoadingSkeleton className="min-h-[100px]" />
  </Section>
);

export const Callouts = () => (
  <Section name="Callout">
    <Callout level="tip">tip</Callout>
    <Callout level="info">info</Callout>
    <Callout level="warn">warn</Callout>
  </Section>
);
