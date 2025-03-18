"use client";

import Link from "next/link";
import React, { ComponentPropsWithoutRef } from "react";
import Icon, { type AppIcon } from "@/components/icon";
import { ChildrenProps, ClassNameProps } from "@/types/react";
import { addClass } from "@/util/transforms";

/**
 * A button with no padding.
 */
export const InlineButton = (props: ButtonProps) => {
  const { children, ...rest } = addClass(
    props,
    "relative rounded-sm font-bold tracking-tight hover:[&_.outofbounds]:bg-hover",
  );
  return (
    <BaseButton {...rest}>
      <div className="absolute -inset-x-2 -inset-y-1 pointer-events-none outofbounds rounded-lg transition-colors" />
      {children}
    </BaseButton>
  );
};

export const Button = (props: ButtonProps) => {
  const { ...rest } = addClass(
    props,
    "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
    "font-bold transition-colors",
    "hover:bg-hover_surface",
  );

  return <BaseButton {...rest} />;
};

export const TintedButton = (props: ButtonProps) => {
  const { style, ...rest } = addClass(props, "surface");

  const themedStyle = {
    ...style,
    "--surface": "var(--vibrant)",
    "--on_surface": "var(--on_vibrant)",
  };

  return <Button style={themedStyle} {...rest} />;
};

interface ButtonContentProps {
  icon?: AppIcon;
}

export type ButtonLinkProps = {
  href: string | null | undefined;
} & ButtonContentProps &
  Omit<ComponentPropsWithoutRef<"a">, "onClick" | "href">;
type ButtonDivProps = ButtonContentProps &
  Omit<ComponentPropsWithoutRef<"a">, "onClick">;
export type ButtonProps =
  | (ButtonContentProps & ComponentPropsWithoutRef<"button">)
  | ButtonDivProps
  | ButtonLinkProps;

const isLink = (
  obj: any,
): obj is ComponentPropsWithoutRef<"a"> & { href: string } => {
  return "href" in obj && obj.href;
};
const isButton = (obj: any): obj is ComponentPropsWithoutRef<"button"> => {
  return (
    ("onClick" in obj && typeof obj.onClick === "function") ||
    ("type" in obj && obj.type === "submit")
  );
};

const ButtonContent = (props: ButtonContentProps & ChildrenProps) => {
  const { icon, children } = props;

  if (icon && React.Children.count(children) === 0)
    return <ButtonIcon icon={icon} />;

  return (
    <div className="flex items-center gap-1 overflow-hidden *:shrink-0">
      <ButtonIcon icon={icon} />
      {children}
    </div>
  );
};

const ButtonIcon = (props: ButtonContentProps & ClassNameProps) => (
  <Icon {...addClass(props, "fill-current/90")} />
);

const BaseButton = (props: ButtonProps) => {
  const { icon, children, ..._rest } = addClass(
    props,
    "relative inline-flex items-center justify-center hover:cursor-pointer transition-all select-none",
  );

  const isIconOnly = icon && React.Children.count(children) === 0;
  const content = (
    <>
      <span className="absolute size-full touch-target pointer:hidden bg-red-500/50" />
      {isIconOnly ? (
        <ButtonIcon icon={icon} />
      ) : (
        <ButtonContent icon={icon}>{children}</ButtonContent>
      )}
    </>
  );

  const rest = isIconOnly ? addClass(_rest, "aspect-square") : _rest;

  if (isLink(rest)) {
    return <Link {...rest}>{content}</Link>;
  }
  if (isButton(rest)) {
    return <button {...rest}>{content}</button>;
  }

  // No usable href or onClick - render as simple div.
  return (
    <div
      {...(addClass(
        rest,
        "pointer-events-none",
      ) as ComponentPropsWithoutRef<"div">)}
    >
      {content}
    </div>
  );
};
