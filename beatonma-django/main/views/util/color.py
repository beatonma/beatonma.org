import colorsys
from typing import NamedTuple

from main.models.mixins import ThemeableMixin

__all__ = [
    "get_theme_context",
]

CSS_TEMPLATE = """:root {{
{content}
}}"""
CSS_ATTR_SEPARATOR = ""


RGB = NamedTuple("RGB", [("red", float), ("green", float), ("blue", float)])
HLS = NamedTuple("HLS", [("hue", float), ("luminance", float), ("saturation", float)])


def get_theme_context(*themeable: ThemeableMixin) -> dict:
    style = get_themeable_css(*themeable)
    if style:
        result = CSS_TEMPLATE.format(content=style)
        return {"local_style": result}
    return {}


def get_themeable_css(*themeable: ThemeableMixin) -> str:
    muted = None
    vibrant = None

    for item in themeable:
        if not item:
            continue

        muted = item.color_muted
        vibrant = item.color_vibrant

        if muted and vibrant:
            break

    colors = []

    if muted:
        colors.append(generate_color_variants(str(muted)).to_css("muted"))

    if vibrant:
        colors.append(generate_color_variants(str(vibrant)).to_css("vibrant"))

    return CSS_ATTR_SEPARATOR.join(colors)


class ColorVariants:
    base: str
    on_base: str
    hover: str
    on_hover: str
    dark: str
    dark_hover: str
    light: str
    light_hover: str

    def __init__(
        self,
        base: str,
        on_base: str,
        hover: str,
        on_hover: str,
        dark: str,
        dark_hover: str,
        light: str,
        light_hover: str,
    ):
        self.base = base
        self.on_base = on_base
        self.hover = hover
        self.on_hover = on_hover
        self.dark = dark
        self.dark_hover = dark_hover
        self.light = light
        self.light_hover = light_hover

    def to_css(self, label: str, joiner: str = CSS_ATTR_SEPARATOR) -> str:
        return joiner.join(
            [
                _css_var(label, self.base),
                _css_var(f"on-{label}", self.on_base),
                _css_var(f"{label}-hover", self.hover),
                _css_var(f"on-{label}-hover", self.on_hover),
                _css_var(f"{label}-dark", self.dark),
                _css_var(f"{label}-dark-hover", self.dark_hover),
                _css_var(f"{label}-light", self.light),
                _css_var(f"{label}-light-hover", self.light_hover),
            ]
        )


def generate_color_variants(hex_color: str) -> ColorVariants:
    main = hex_to_hls(hex_color)
    main_hover = _hover(main)

    lighter = _lighter(main)
    lighter_hover = _hover(lighter)

    darker = _darker(main)
    darker_hover = _hover(darker)

    on_main = _on(main)
    on_main_hover = _hover(on_main)

    return ColorVariants(
        base=hls_to_hex(main),
        on_base=hls_to_hex(on_main),
        hover=hls_to_hex(main_hover),
        on_hover=hls_to_hex(on_main_hover),
        dark=hls_to_hex(darker),
        dark_hover=hls_to_hex(darker_hover),
        light=hls_to_hex(lighter),
        light_hover=hls_to_hex(lighter_hover),
    )


def hex_to_rgb(hexstr: str) -> RGB:
    def _component(c: str) -> float:
        return float(int(c, 16)) / 255.0

    return RGB(
        _component(hexstr[1:3]),
        _component(hexstr[3:5]),
        _component(hexstr[5:7]),
    )


def hex_to_hls(hexstr: str) -> HLS:
    rgb = hex_to_rgb(hexstr)
    return rgb_to_hls(rgb)


def hls_to_hex(hls: HLS) -> str:
    rgb = hls_to_rgb(hls)
    return rgb_to_hex(rgb)


def hls_to_rgb(hls: HLS) -> RGB:
    return RGB(*colorsys.hls_to_rgb(*hls))


def rgb_to_hex(rgb: RGB) -> str:
    def _float_to_hex(component: float) -> str:
        return f"{int(component * 255.0):0{2}x}"

    return f"#{''.join([_float_to_hex(x) for x in rgb])}"


def rgb_to_hls(rgb: RGB) -> HLS:
    return HLS(*colorsys.rgb_to_hls(*rgb))


def _perceived_luminance(rgb: RGB) -> float:
    return 0.299 * rgb.red + 0.587 * rgb.green + 0.114 * rgb.blue


def _tweak(
    value: float,
    center: float = 0.5,
    variance: float = 0.05,
    keep_grayscale: bool = False,
) -> float:
    """Alter the value towards center by variance."""

    if keep_grayscale and (value == 0 or value == 1):
        return value

    if value > center:
        return value - variance
    return value + variance


def _darker(hls: HLS) -> HLS:
    return HLS(hls.hue, 0.2, hls.saturation)


def _lighter(hls: HLS) -> HLS:
    return HLS(hls.hue, 0.8, hls.saturation)


def _hover(hls: HLS) -> HLS:
    return HLS(
        hls.hue,
        _tweak(hls.luminance),
        _tweak(hls.saturation, keep_grayscale=True),
    )


def _on(hls: HLS) -> HLS:
    rgb = hls_to_rgb(hls)
    perceived_luminance = _perceived_luminance(rgb)

    return HLS(
        hls.hue,
        0.1 if perceived_luminance >= 0.5 else 0.9,
        hls.saturation,
    )


def _css_var(name: str, hex_value: str) -> str:
    return f"--{name}:{hex_value}!important;"
