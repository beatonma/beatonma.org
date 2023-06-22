import colorsys
from typing import List, NamedTuple

from colorfield.fields import ColorField
from main.models.mixins import ThemeableMixin

__all__ = [
    "get_theme_context",
]

CSS_TEMPLATE = """:root {{
{content}
}}"""


def get_theme_context(*themeable: ThemeableMixin) -> dict:
    style = _find_theme(*themeable)
    if style:
        result = CSS_TEMPLATE.format(content="\n".join(style))
        return {"local_style": result}
    return {}


RGB = NamedTuple("RGB", [("red", float), ("green", float), ("blue", float)])
HLS = NamedTuple("HLS", [("hue", float), ("luminance", float), ("saturation", float)])


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
    return f"--{name}: {hex_value} !important;"


def _generate_variants(
    label: str,
    colorfield: ColorField,
) -> List[str]:
    hexcolor = str(colorfield)

    main = hex_to_hls(hexcolor)
    main_hover = _hover(main)

    lighter = _lighter(main)
    lighter_hover = _hover(lighter)

    darker = _darker(main)
    darker_hover = _hover(darker)

    on_main = _on(main)
    on_main_hover = _hover(on_main)

    return [
        _css_var(label, hls_to_hex(main)),
        _css_var(f"{label}-hover", hls_to_hex(main_hover)),
        _css_var(f"{label}-dark", hls_to_hex(darker)),
        _css_var(f"{label}-dark-hover", hls_to_hex(darker_hover)),
        _css_var(f"{label}-light", hls_to_hex(lighter)),
        _css_var(f"{label}-light-hover", hls_to_hex(lighter_hover)),
        _css_var(f"on-{label}", hls_to_hex(on_main)),
        _css_var(f"on-{label}-hover", hls_to_hex(on_main_hover)),
    ]


def _find_theme(*themeable: ThemeableMixin) -> List[str]:
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
        colors += _generate_variants("muted", muted)

    if vibrant:
        colors += _generate_variants("vibrant", vibrant)

    return colors
