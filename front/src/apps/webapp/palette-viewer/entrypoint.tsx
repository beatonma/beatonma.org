import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./palette-viewer.scss";
import { ThemeToggle } from "../../main/js/components/theme-toggle";

const CONTAINER_ID: string = "palette-viewer_container";

const PaletteViewer = () => {
    const [colors, setColors] = useState<string[]>([]);
    const [colorsInput, setColorsInput] = useState(
        formatColorInput("--red --green --blue --purple 000000 #ffffff33")
    );

    useEffect(() => {
        parseColors(colorsInput)
            .then(colors => {
                console.log(colors);
                return colors;
            })
            .then(setColors);
    }, [colorsInput]);

    return (
        <main>
            <h1>Palettes</h1>
            <ThemeToggle />

            <textarea
                value={colorsInput}
                placeholder="hex strings here"
                onChange={e => setColorsInput(formatColorInput(e.target.value))}
            />

            <div id="palette">
                <Colors colors={colors} />
            </div>
        </main>
    );
};

const Colors = (props: { colors: string[] }) => {
    if (props.colors.length === 0) return <div></div>;

    return (
        <>
            {props.colors.map((color, index) => (
                <div style={{ backgroundColor: color }} key={index}>
                    <div className="color">
                        {color.replace(/(var|[)(])/g, "")}
                    </div>
                </div>
            ))}
        </>
    );
};

const parseColors = async (input: string): Promise<string[]> => {
    const colorCodes = [...input.matchAll(/(#?([a-fA-F0-9]+)|--[\w-]+)/g)]
        .map(match => {
            const hex = match[2];
            if (hex) {
                return [3, 6, 8].includes(hex.length)
                    ? `#${hex}`.toLowerCase()
                    : null;
            }

            const _var = match[1];
            return `var(${_var})`;
        })
        .filter(it => !!it);

    return colorCodes;
};

const formatColorInput = (input: string): string =>
    input
        .replace(/(?!\s+)#/g, "\n#")
        .replace(/\s+/g, "\n")
        .replace(/((?:^.*$\s){4})/gm, "$1\n");

const attachApp = (dom: Document | Element = document) => {
    const container = dom.querySelector(`#${CONTAINER_ID}`);

    if (container) {
        const root = createRoot(container);
        root.render(<PaletteViewer />);
    } else {
        console.warn(`Root container not found! #${CONTAINER_ID}`);
    }
};

attachApp();
