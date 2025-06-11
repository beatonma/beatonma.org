"use client";

import { ComponentPropsWithoutRef, useCallback } from "react";
import {
  Button,
  InlineButton,
  InlineLink,
  TintedButton,
} from "@/components/button";
import { Callout } from "@/components/callout";
import { Icon } from "@/components/icon";
import { _private as Icon_private } from "@/components/icon/bundled";
import { Row } from "@/components/layout";
import {
  LoadingBar,
  LoadingSkeleton,
  LoadingSpinner,
} from "@/components/loading";
import { ClassNameProps } from "@/types/react";
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

export const Buttons = () => {
  const onClick = useCallback(() => console.log("click"), []);
  return (
    <Section name="Buttons" className="space-y-2">
      <Row className="gap-4 flex-wrap">
        <InlineButton icon="MB" href="#" />
        <InlineButton href="#">InlineButton</InlineButton>
        <InlineButton onClick={onClick} icon="MB">
          InlineButton
        </InlineButton>
        <InlineButton disabled onClick={onClick} icon="MB">
          disabled
        </InlineButton>
        <InlineButton tooltip="Tooltip" onClick={onClick}>
          Tooltip
        </InlineButton>
      </Row>

      <Row className="gap-4 flex-wrap">
        <TintedButton icon="MB" href="#" />
        <TintedButton href="#">TintedButton</TintedButton>
        <TintedButton onClick={onClick} icon="MB">
          TintedButton
        </TintedButton>
        <TintedButton disabled onClick={onClick} icon="MB">
          disabled
        </TintedButton>
        <TintedButton tooltip="Tooltip" onClick={onClick}>
          Tooltip
        </TintedButton>
      </Row>

      <Row className="gap-4 flex-wrap">
        <Button icon="MB" href="#" />
        <Button href="#">Button</Button>
        <Button onClick={onClick} icon="MB">
          Button
        </Button>
        <Button disabled onClick={onClick} icon="MB">
          disabled
        </Button>
        <Button tooltip="This is a really long tooltip" onClick={onClick}>
          Tooltip
        </Button>
      </Row>

      <Row className="gap-4 flex-wrap">
        <InlineLink icon="MB" href="https://beatonma.org" />
        <InlineLink href="https://beatonma.org" />
        <InlineLink tooltip="Tooltip" href="https://beatonma.org" />
      </Row>
    </Section>
  );
};
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
    <LoadingSpinner />
    <LoadingBar />
    <LoadingBar progress={64} />
    <LoadingSkeleton className="min-h-[100px]" />
  </Section>
);

export const Callouts = () => (
  <Section name="Callout">
    <Callout level="tip">tip</Callout>
    <Callout level="info">info</Callout>
    <Callout level="important">important</Callout>
    <Callout level="warn">warn</Callout>
    <Callout level="caution">caution</Callout>
  </Section>
);

export const Surfaces = () => {
  const Surface = (props: ClassNameProps) => {
    const content = (
      <>
        <strong>{props.className}</strong>
        <p>
          A paragraph of text with a <a href="#">link</a>.
        </p>
        <Row className="gap-2">
          <Button icon="MB" className="surface" />
          <Button icon="MB" className="surface-alt" />
          <Button icon="MB" className="surface-vibrant" />
          <Button icon="MB" className="surface-muted" />
        </Row>
      </>
    );
    return (
      <>
        <div {...addClass(props, "card card-content readable prose")}>
          {content}
        </div>
      </>
    );
  };

  return (
    <Section name="Surfaces">
      <div className="space-y-4 max-w-[40ch]">
        <Surface className="background" />
        <Surface className="surface" />
        <Surface className="surface-alt" />
        <Surface className="surface-vibrant" />
        <Surface className="surface-muted" />
      </div>
    </Section>
  );
};
