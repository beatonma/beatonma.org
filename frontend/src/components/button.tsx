"use client";

import Link from "next/link";
import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import Icon, { type AppIcon } from "@/components/icon";
import { ChildrenProps, ClassNameProps } from "@/types/react";
import { addClass, formatUrl } from "@/util/transforms";

interface ButtonContentProps {
  icon?: AppIcon | ReactNode;
}
interface ButtonColors {
  colors?: string;
}

type ButtonLinkProps = {
  href: string | null | undefined;
} & ButtonContentProps &
  Omit<ComponentPropsWithoutRef<"a">, "onClick" | "href">;

type ButtonProps = ButtonContentProps &
  (
    | ComponentPropsWithoutRef<"button">
    | Omit<ComponentPropsWithoutRef<"a">, "onClick">
    | Omit<ComponentPropsWithoutRef<"div">, "onClick">
  );

/**
 * A button with no padding which shows a larger background on hover.
 */
export const InlineButton = (props: ButtonProps) => {
  const { children, ...rest } = addClass(
    props,
    "relative select-none no-underline! rounded-sm font-bold tracking-tight",
    "hover:[&_.outofbounds]:bg-hover",
    "disabled:[&_.outofbounds]:hidden",
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

/**
 * A typical button with customisable colors.
 */
export const Button = (props: ButtonProps & ButtonColors) => {
  const { colors, ...rest } = addClass(
    props,
    "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
    "select-none font-bold no-underline!",
  );
  return (
    <BaseButton colors={colors || "hover:not-disabled:bg-hover"} {...rest} />
  );
};

/**
 * A button styled with the current `vibrant` theme color.
 */
export const TintedButton = (props: ButtonProps) => {
  return <Button colors="surface-vibrant hover-surface-vibrant" {...props} />;
};

/**
 * A typical link with automatic formatting and optional icon.
 */
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

const BaseButton = (
  props: ButtonProps & ButtonColors & { background?: ReactNode },
) => {
  const {
    icon,
    colors: _colors,
    background,
    children,
    ...rest
  } = addClass(
    props,
    "relative transition-all",
    "inline-flex items-center justify-center",
    "hover:cursor-pointer",
    "disabled:cursor-not-allowed disabled:contrast-40",
    props.colors,
  );

  const content = (
    <>
      <span className="absolute size-full touch-target pointer:hidden" />
      {background}
      <ButtonContent icon={icon}>{children}</ButtonContent>
    </>
  );

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

const isLink = (
  obj: any,
): obj is { href: string } & ComponentPropsWithoutRef<"a"> => {
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
