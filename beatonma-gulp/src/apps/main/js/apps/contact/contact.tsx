import { Scaffold } from "../../dom";
import { Theme } from "../../theme";
import React, { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import { getCsrfToken } from "../../util/cookies";
import { useTextEventListener } from "../../util/listeners";
import { searchParams } from "../../util/location";

const CONTAINER_ID = "contact";
const ERROR_MESSAGE_ID = "error_response";
const FORM_ID = "contact_form";
const BUTTON_ID = "contact_submit";

const NAME_ID = "contact_name";
const MESSAGE_BODY_ID = "contact_message";

export const ContactApp = (dom: Document | Element) => {
    const container = dom.querySelector(`#${CONTAINER_ID}`);

    if (container) {
        setup();
    }
};

const setSubmitButtonEnabled = (enabled: boolean) => {
    (document.getElementById(BUTTON_ID) as HTMLButtonElement).disabled =
        !enabled;
};

const onCaptchaPassed = () => {
    setSubmitButtonEnabled(true);
};

const onCaptchaExpired = () => {
    setSubmitButtonEnabled(false);
};

const onSubmitContact = (event: SubmitEvent): boolean => {
    event.preventDefault();
    Scaffold.showLoading(true);

    const contact = document.getElementById(FORM_ID) as HTMLFormElement;
    const form = new FormData(contact);
    const csrftoken = getCsrfToken();
    const headers = new Headers({ "X-CSRFToken": csrftoken });

    fetch("/contact/send/", {
        headers: headers,
        method: "POST",
        body: form,
        credentials: "same-origin",
    })
        .then(response => {
            Scaffold.showLoading(false);

            if (response.ok) {
                renderSuccess();
            } else {
                renderError(response.statusText, response.status);
            }
        })
        .catch(err => {
            console.error(err);
            renderError(err);
        });

    return false;
};

const renderSuccess = () => {
    const container = document.getElementById(CONTAINER_ID);
    if (container) {
        const root = createRoot(container);
        root.render(
            <StrictMode>
                <ContactSuccessful />
            </StrictMode>
        );
    }
};

const renderError = (message: string, status?: number) => {
    const container = document.getElementById(ERROR_MESSAGE_ID);
    if (container) {
        const root = createRoot(container);
        root.render(
            <StrictMode>
                <ContactError errorMessage={message} status={status} />
            </StrictMode>
        );
    }
};

const ContactSuccessful = () => {
    return (
        <div className="success">
            <h2>Thank you!</h2>
            <p>
                Your message has been submitted successfully - I will get back
                to you as soon as possible.
            </p>
        </div>
    );
};

interface ContactErrorProps {
    errorMessage?: string;
    status?: number;
}
const ContactError = (props: ContactErrorProps) => {
    const { errorMessage, status } = props;

    const [message, setMessage] = useState(
        encodeURIComponent(
            (document.getElementById(MESSAGE_BODY_ID) as HTMLTextAreaElement)
                .value
        )
    );

    useTextEventListener(
        MESSAGE_BODY_ID,
        (value: string) => setMessage(encodeURIComponent(value)),
        "change"
    );

    const subject = encodeURIComponent("__env__:siteName webmail");

    console.error(`Message submission failed: ${errorMessage}`);

    return (
        <div className="failure">
            {status ? <h3>[{status}] Submission failed.</h3> : <></>}
            <p>It looks like something went wrong. Sorry about that!</p>
            <p>
                Please{" "}
                <a
                    href={`mailto:__env__:contactEmail?subject=${subject}&body=${message}`}
                >
                    email me instead
                </a>{" "}
                :)
            </p>
        </div>
    );
};

const setup = () => {
    document
        .querySelectorAll(".g-recaptcha")
        .forEach(
            (el: HTMLElement) =>
                (el.dataset.theme = Theme.isDark() ? "dark" : "light")
        );

    document.getElementById(NAME_ID).focus();

    window.onSubmitContact = onSubmitContact;
    window.onContactCaptchaPassed = onCaptchaPassed;
    window.onContactCaptchaExpired = onCaptchaExpired;

    const devState = searchParams().get("debug");
    const debugging: Record<string, () => void> = {
        success: renderSuccess,
        fail: () => renderError("Debug message please ignore :)", 418),
    };
    debugging[devState]?.();
};

declare global {
    interface Window {
        onSubmitContact: (event: Event) => void;
        onContactCaptchaPassed: (token: string) => void;
        onContactCaptchaExpired: () => void;
    }
}
