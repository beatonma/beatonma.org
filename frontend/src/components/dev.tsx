import Callout from "@/components/callout";
import { DivProps } from "@/types/react";
import { useEffect } from "react";

export default function Todo(props: DivProps) {
    const { children, ...rest} = props;

    useEffect(() => {
        console.log(`TODO ${children}`)
    }, []);

    return <Callout level="warn" {...rest}>
        <strong>TODO</strong>
        {children}
    </Callout>
}
