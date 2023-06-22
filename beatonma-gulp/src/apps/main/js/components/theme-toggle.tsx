import React from "react";
import { Theme } from "../theme";

export const ThemeToggle = () => (
    <button id={Theme.ID_TOGGLE_BUTTON} onClick={Theme.toggle}></button>
);
