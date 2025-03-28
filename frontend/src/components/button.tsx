"use client";

import Link from "next/link";
import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import Icon, { type AppIcon } from "@/components/icon";
import { ChildrenProps, ClassNameProps } from "@/types/react";
import { addClass, formatUrl } from "@/util/transforms";

/**
 * A button with no padding.
 */
export const InlineButton = (props: ButtonProps) => {
  const { children, ...rest } = addClass(
    props,
    "relative select-none no-underline! rounded-sm font-bold tracking-tight",
    "hover:not-disabled:[&_.outofbounds]:bg-hover",
    "disabled:text-current/70 disabled:fill-current/70",
  );
  return (
    <BaseButton
      background={
        <div className="absolute -inset-x-2 -inset-y-1 pointer-events-none outofbounds rounded-lg transition-colors" />
      }
      {...rest}
    >
      {children}
    </BaseButton>
  );
};

export const Button = (props: ButtonProps) => {
  return (
    <BaseButton
      {...addClass(
        props,
        "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
        "select-none font-bold transition-colors no-underline!",
        "hover:not-disabled:bg-hover",
        "disabled:text-current/70 disabled:fill-current/70",
      )}
    />
  );
};

export const TintedButton = (props: ButtonProps) => {
  const { style, ...rest } = addClass(
    props,
    "surface",
    "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
    "select-none font-bold transition-colors no-underline!",
    "hover:not-disabled:bg-[color-mix(in_srgb,var(--surface)_85%,currentColor)]",
    "disabled:grayscale-75 disabled:text-on-vibrant/50 disabled:fill-on-vibrant/50",
  );

  const themedStyle = {
    ...style,
    "--surface": "var(--vibrant)",
    "--on-surface": "var(--on-vibrant)",
  };

  return <BaseButton style={themedStyle} {...rest} />;
};

export const InlineLink = (props: ButtonLinkProps) => {
  const { href, children, icon, ...rest } = addClass(props, "hover:underline");
  if (!href) return null;

  return (
    <BaseButton
      href={href}
      icon={icon === null ? null : (icon ?? "Link")}
      {...rest}
    >
      {children ?? formatUrl(href)}
    </BaseButton>
  );
};

interface ButtonContentProps {
  icon?: AppIcon | ReactNode;
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
    <div className="grid grid-cols-[auto_1fr] items-center overflow-hidden">
      <ButtonIcon icon={icon} className="me-1" />
      <div className="col-start-2 overflow-hidden overflow-ellipsis line-clamp-1 break-all">
        {children}
      </div>
    </div>
  );
};

const ButtonIcon = (props: ButtonContentProps & ClassNameProps) => {
  const { icon, ...rest } = addClass(props, "fill-current/90");

  if (!icon) return null;

  if (typeof icon === "string") {
    return <Icon icon={icon as AppIcon} {...rest} />;
  }

  return <div {...addClass(rest, "size-em overflow-hidden")}>{icon}</div>;
};

const BaseButton = (props: ButtonProps & { background?: ReactNode }) => {
  const { icon, background, children, ..._rest } = addClass(
    props,
    "relative inline-flex items-center justify-center hover:not-disabled:cursor-pointer transition-all",
    "disabled:cursor-not-allowed",
  );

  const isIconOnly = icon && React.Children.count(children) === 0;
  const content = (
    <>
      <span className="absolute size-full touch-target pointer:hidden" />
      {background}
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
