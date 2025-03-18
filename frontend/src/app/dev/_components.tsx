"use client";

import { ComponentPropsWithoutRef } from "react";
import { SampleMedia } from "@/app/dev/_sample";
import { Button, InlineButton, TintedButton } from "@/components/button";
import Icon, { _private as Icon_private } from "@/components/icon";
import { Row } from "@/components/layout";
import Loading, { LoadingBar } from "@/components/loading";
import MediaCarousel from "@/components/media/media-carousel";
import { addClass } from "@/util/transforms";

const Section = (props: ComponentPropsWithoutRef<"section">) => (
  <section {...addClass(props, " gap-4 items-start")} />
);

export const Buttons = () => (
  <Section>
    <Row className="gap-4 flex-wrap">
      <InlineButton href="#">InlineButton</InlineButton>
      <InlineButton onClick={() => console.log("click")} icon="MB">
        InlineButton
      </InlineButton>

      <TintedButton href="#">TintedButton</TintedButton>
      <TintedButton onClick={() => console.log("click")} icon="MB">
        TintedButton
      </TintedButton>

      <Button href="#">Button</Button>
      <Button onClick={() => console.log("click")} icon="MB">
        Button
      </Button>
    </Row>
  </Section>
);
export const Icons = () => {
  const icons = Icon_private.Icons;

  return (
    <Section>
      <div className="card card-content surface grid grid-cols-[repeat(auto-fit,96px)] gap-2">
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
  <Section>
    <Loading />
    <LoadingBar />
  </Section>
);

export const Media = () => <MediaCarousel media={SampleMedia} />;
