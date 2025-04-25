export enum H {
  "h-card" = "h-card",
  "h-adr" = "h-adr",
}

/**
 * Known fields for an h-card.
 */
export enum HCard {
  "dt-bday" = "dt-bday",
  "p-name" = "p-name",
  "p-locality" = "p-locality",
  "p-region" = "p-region",
  "p-country-name" = "p-country-name",
  "u-email" = "u-email",
  "u-logo" = "u-logo",
  "u-photo" = "u-photo",
  "u-url" = "u-url",
}

export type Microformat = keyof typeof H | keyof typeof HCard;
