export const ID_THEME_TOGGLE_BUTTON = "theme_icon";
const CLASS_DARK = "dark";
const CLASS_LIGHT = "light";
const SCHEME_MEDIA_QUERY = "(prefers-color-scheme: dark)";
const STORAGE_THEME = "darkTheme";

let _isDark: boolean = null;
export namespace Theme {
    export const EVENT_THEME_CHANGED = "themechange";
    export const ID_TOGGLE_BUTTON = "theme_icon";

    export const toggle = async () => setDark(!_isDark);
    export const isDark = (): boolean => _isDark;
}
const onThemeChangeEvent = new Event(Theme.EVENT_THEME_CHANGED);

const loadTheme = () => {
    const storedIsDark: boolean = JSON.parse(
        window.localStorage.getItem(STORAGE_THEME)
    );

    if (storedIsDark === null) {
        _isDark = window.matchMedia(SCHEME_MEDIA_QUERY).matches;
    } else {
        _isDark = storedIsDark;
    }

    void setDark(_isDark, false);
};

const setDark = async (dark: boolean, save: boolean = true) => {
    _isDark = dark;
    document.documentElement.classList.add(dark ? CLASS_DARK : CLASS_LIGHT);
    document.documentElement.classList.remove(dark ? CLASS_LIGHT : CLASS_DARK);

    window.dispatchEvent(onThemeChangeEvent);

    if (save) {
        window.localStorage.setItem(STORAGE_THEME, `${_isDark}`);
    }
};

try {
    loadTheme();

    window
        .matchMedia(SCHEME_MEDIA_QUERY)
        .addEventListener("change", event => setDark(event.matches, false));

    document
        .getElementById(ID_THEME_TOGGLE_BUTTON)
        .addEventListener("click", Theme.toggle);
} catch (e) {
    console.error(e);
}
