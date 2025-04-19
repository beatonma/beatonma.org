"use client";

import React, { ReactNode } from "react";
import Icon, { type AppIcon } from "@/components/icon";
import ExternalLink from "@/components/third-party/link";
import { useTooltip } from "@/components/tooltip/tooltip";
import { Nullish } from "@/types";
import {
  ChildrenProps,
  ClassNameProps,
  DivProps,
  Props,
  PropsExcept,
} from "@/types/react";
import { addClass, formatUrl } from "@/util/transforms";

interface ButtonContentProps {
  icon?: AppIcon | ReactNode;
  tooltip?: string;
}
interface ButtonColors {
  colors?: string;
}

type ButtonLinkProps = ButtonContentProps &
  PropsExcept<typeof ExternalLink, "onClick" | "href"> & {
    href: string | Nullish;
  };

export type ButtonProps = ButtonContentProps &
  (Props<"button"> | ButtonLinkProps | PropsExcept<"div", "onClick">);

/**
 * A button with no padding which shows a larger background on hover.
 */
export const InlineButton = (props: ButtonProps) => {
  const { children, ...rest } = addClass(
    props,
    "relative select-none no-underline! rounded-sm font-bold tracking-tight",
    "hover-extra-background before:-inset-x-2 before:-inset-y-1",
  );
  return <BaseButton {...rest}>{children}</BaseButton>;
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

  return (
    <BaseButton
      href={href ?? undefined}
      icon={icon === null ? null : (icon ?? "Link")}
      {...rest}
    >
      {children ?? formatUrl(href)}
    </BaseButton>
  );
};

const BaseButton = (props: ButtonProps & ButtonColors) => {
  const {
    icon,
    tooltip,
    colors: _colors,
    children,
    ...rest
  } = addClass(
    props,
    "isolate relative transition-all",
    "inline-flex items-center justify-center",
    "hover:cursor-pointer",
    "disabled:cursor-not-allowed disabled:contrast-40",
    props.colors,
  );

  const tooltipAttrs = useTooltip({ tooltip });

  const content = (
    <>
      <span className="absolute size-full touch-target pointer:hidden" />
      <ButtonContent icon={icon}>{children}</ButtonContent>
    </>
  );

  if (isLink(rest)) {
    return (
      <ExternalLink {...rest} {...tooltipAttrs}>
        {content}
      </ExternalLink>
    );
  }
  if (isButton(rest)) {
    return (
      <button {...rest} {...tooltipAttrs}>
        {content}
      </button>
    );
  }

  // Strip any `hover:` or `hover-` classes from className. Don't use
  //   `pointer-events-none` as that prevents tooltip from working.
  const { className: originalClassName, ...divRest } = addClass(
    rest,
    "cursor-default",
  ) as DivProps;
  const noHoverClassName = originalClassName?.replace(
    /(^|\s+)hover[-:]\S+/g,
    "",
  );

  // No usable href or onClick - render as simple div.
  return (
    <div className={noHoverClassName} {...divRest} {...tooltipAttrs}>
      {content}
    </div>
  );
};

const isLink = (
  obj: any,
): obj is { href: string } & Props<typeof ExternalLink> => {
  return "href" in obj && obj.href;
};
const isButton = (obj: any): obj is Props<"button"> => {
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
