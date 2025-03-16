"use client";

import Link from "next/link";
import React, { ComponentPropsWithoutRef } from "react";
import Icon, { type AppIcon } from "@/components/icon";
import { ChildrenProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const TextButton = (props: ButtonProps) => {
  const { children, ...rest } = addClass(
    props,
    "relative rounded-sm font-bold tracking-tight hover:[&_.outofbounds]:bg-hover",
  );
  return (
    <BaseButton {...rest}>
      <div className="absolute -inset-1/6 pointer-events-none outofbounds rounded-lg transition-colors" />
      {children}
    </BaseButton>
  );
};

export const TintedButton = (props: ButtonProps) => {
  const { style, ...rest } = addClass(
    props,
    "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
    "surface font-bold transition-colors",
    "hover:bg-[color-mix(in_srgb,var(--surface)_90%,var(--on_surface))]",
  );

  const themedStyle = {
    ...style,
    "--surface": "var(--vibrant)",
    "--on_surface": "var(--on_vibrant)",
  };

  return <BaseButton style={themedStyle} {...rest} />;
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
    <div className="flex items-center gap-1">
      <ButtonIcon icon={icon} />
      {children}
    </div>
  );
};

const ButtonIcon = (props: ButtonContentProps) => (
  <Icon className="fill-current/90" {...props} />
);

const BaseButton = (props: ButtonProps) => {
  const { icon, children, ..._rest } = addClass(
    props,
    "inline-flex items-center justify-center hover:cursor-pointer transition-all touch-target select-none",
  );

  const isIconOnly = icon && React.Children.count(children) === 0;
  const content = isIconOnly ? (
    <ButtonIcon icon={icon} />
  ) : (
    <ButtonContent icon={icon}>{children}</ButtonContent>
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
