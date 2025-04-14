import { CSSProperties, ComponentPropsWithoutRef } from "react";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import BlueSky from "./svg/external/ic_bluesky.svg";
import Facebook from "./svg/external/ic_facebook.svg";
import Github from "./svg/external/ic_github.svg";
import Instagram from "./svg/external/ic_instagram.svg";
import Twitter from "./svg/external/ic_twitter.svg";
import Wikipedia from "./svg/external/ic_wikipedia.svg";
import MB from "./svg/internal/mb.svg";
import ArrowDown from "./svg/material/arrow_down.svg";
import ArrowUp from "./svg/material/arrow_up.svg";
import Attachment from "./svg/material/attachment.svg";
import Check from "./svg/material/check.svg";
import ChevronLeft from "./svg/material/chevron_left.svg";
import ChevronRight from "./svg/material/chevron_right.svg";
import Close from "./svg/material/close.svg";
import Code from "./svg/material/code.svg";
import GitBranch from "./svg/material/git_branch.svg";
import GitBugfix from "./svg/material/git_bugfix.svg";
import GitCommit from "./svg/material/git_commit.svg";
import GitMerge from "./svg/material/git_merge.svg";
import GitRelease from "./svg/material/git_release.svg";
import GitWiki from "./svg/material/git_wiki.svg";
import Audio from "./svg/material/headphones.svg";
import Home from "./svg/material/home.svg";
import Image from "./svg/material/image.svg";
import Link from "./svg/material/link.svg";
import Email from "./svg/material/mail.svg";
import PlayArrow from "./svg/material/play_arrow.svg";
import QuestionMark from "./svg/material/questionmark.svg";
import Search from "./svg/material/search.svg";
import Tag from "./svg/material/tag.svg";
import Text from "./svg/material/text.svg";
import ThemeDarkMode from "./svg/material/theme_darkmode.svg";
import ThemeSystemDefault from "./svg/material/theme_default.svg";
import ThemeLightMode from "./svg/material/theme_lightmode.svg";

const Icons = {
  // Branding
  MB,

  // Third party branding
  BlueSky,
  Facebook,
  Github,
  Instagram,
  Twitter,
  Wikipedia,

  // App UI
  ThemeLightMode,
  ThemeDarkMode,
  ThemeSystemDefault,

  // Media
  Audio,
  Attachment,
  Image,
  PlayArrow,
  Text,

  // Git
  GitBranch,
  GitBugfix,
  GitCommit,
  GitMerge,
  GitRelease,
  GitWiki,

  // General use
  ArrowUp,
  ArrowDown,
  Code,
  ChevronLeft,
  ChevronRight,
  Check,
  Close,
  Dev: Code,
  Email,
  Home,
  Link,
  QuestionMark,
  Search,
  Tag,
};
export type AppIcon = keyof typeof Icons;

export type IconProps = {
  icon?: AppIcon | Nullish;
} & ComponentPropsWithoutRef<"svg">;

export default function Icon(props: IconProps) {
  const { icon, ...rest } = props;
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element {...rest} />;
}

export interface RemoteIconProps {
  src: string;
  mask?: boolean;
}
export const RemoteIcon = (props: RemoteIconProps & DivPropsNoChildren) => {
  const { src, mask = true, style, ...rest } = addClass(props, "size-em");

  const maskStyle: CSSProperties = mask
    ? {
        backgroundColor: "currentColor",
        maskImage: `url('${src}')`,
        maskSize: "1em",
      }
    : {
        backgroundImage: `url('${src}')`,
        backgroundSize: "1em",
      };

  return <div style={{ ...style, ...maskStyle }} {...rest} />;
};

export const _private = {
  Icons: Object.keys(Icons) as AppIcon[],
};
