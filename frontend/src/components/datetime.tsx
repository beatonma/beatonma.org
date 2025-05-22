import { ComponentPropsWithoutRef } from "react";
import { Nullish } from "@/types";
import { DivPropsNoChildren } from "@/types/react";
import { addClass, capitalize } from "@/util/transforms";

type ParseableDate = Date | string | number | Nullish;
type DateFormat = "smart" | Intl.DateTimeFormat;
const Locale = "en-gb";

export namespace DateFormat {
  export const MonthDay: Intl.DateTimeFormat = new Intl.DateTimeFormat(Locale, {
    day: "numeric",
    month: "long",
  });
  export const YearMonthDay: Intl.DateTimeFormat = new Intl.DateTimeFormat(
    Locale,
    {
      day: "numeric",
      month: "long",
      year: "numeric",
    },
  );
  export const Default = YearMonthDay;
}

export const parseDate = (dt: ParseableDate): Date | null => {
  if (!dt) return null;
  if (dt instanceof globalThis.Date) return dt;

  const result = new globalThis.Date(dt);

  return isNaN(result.valueOf()) ? null : result;
};

export const formatDate = (
  dt: ParseableDate,
  dateFormat: DateFormat = DateFormat.Default,
): string | null => {
  const parsed = parseDate(dt);
  if (!parsed) return null;

  if (dateFormat !== "smart") {
    return dateFormat.format(parsed);
  }

  // Format date differently depending on relation to current date.
  const now = new globalThis.Date();
  if (now.getFullYear() === parsed.getFullYear()) {
    if (
      now.getMonth() === parsed.getMonth() &&
      now.getDate() === parsed.getDate()
    ) {
      return "Today";
    }
    return DateFormat.MonthDay.format(parsed);
  }

  return DateFormat.YearMonthDay.format(parsed);
};

/**
 * Displays nothing if either date fails to be interpreted as a valid Date.
 */
export const DateRange = (
  props: DivPropsNoChildren<{
    start: ParseableDate;
    end: ParseableDate;
    dateFormat?: DateFormat;
    capitalized?: boolean;
  }>,
) => {
  const {
    start: _start,
    end: _end,
    dateFormat,
    capitalized = true,
    ...rest
  } = addClass(props, "flex gap-x-0.5");
  const start = parseDate(props.start);
  const end = parseDate(props.end);

  if (start && end) {
    return (
      <div {...rest}>
        <Date date={start} dateFormat={dateFormat} />-
        <Date date={end} dateFormat={dateFormat} />
      </div>
    );
  }

  if (start) {
    const prefix = "since";
    return (
      <div {...rest}>
        {`${capitalized ? capitalize(prefix) : prefix}`}{" "}
        <Date date={start} dateFormat={dateFormat} />
      </div>
    );
  }
};

export const Date = (
  props: {
    date: ParseableDate;
    dateFormat?: DateFormat;
  } & Omit<ComponentPropsWithoutRef<"time">, "dateTime" | "children" | "title">,
) => {
  const { date, dateFormat = "smart", ...rest } = props;
  const parsed = parseDate(date);

  if (parsed == null) return null;

  return (
    <time
      dateTime={parsed.toDateString()}
      title={parsed.toDateString()}
      suppressHydrationWarning
      {...rest}
    >
      {formatDate(parsed, dateFormat)}
    </time>
  );
};
