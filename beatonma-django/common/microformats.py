from enum import StrEnum


class HCard(StrEnum):
    # dates
    dt_bday = "dt-bday"
    # values
    p_name = "p-name"
    p_locality = "p-locality"
    p_region = "p-region"
    p_country_name = "p-country-name"
    # links
    u_email = "u-email"
    u_logo = "u-logo"
    u_photo = "u-photo"
    u_url = "u-url"


class HAdr(StrEnum):
    p_locality = "p-locality"
    p_region = "p-region"
    p_country_name = "p-country-name"


type Microformat = HCard | HAdr
