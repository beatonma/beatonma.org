"use client";

import { ChangeEvent, useCallback, useMemo, useState } from "react";
import { client } from "@/api";
import { TintedButton } from "@/components/button";
import { FormField } from "@/components/form";
import { Row } from "@/components/layout";
import Prose from "@/components/prose";
import { ExternalLink, RemoteContent } from "@/components/third-party";
import { testId } from "@/util";
import { onlyIf } from "@/util/optional";
import Recaptcha, { RecaptchaProps } from "./_components/recaptcha";

const TestTarget = {
  ContactForm: "contact_form",
  ContactName: "contact_name",
  ContactMethod: "contact_method",
  ContactMessage: "contact_message",
  ContactSuccess: "contact_success",
};
const TextInputClassName = "w-full";

type ContactFormProps = RecaptchaProps;
export default function ContactPage(props: ContactFormProps) {
  const [isMessageSent, setIsMessageSent] = useState(false);

  return (
    <Prose className="mx-auto readable">
      <h2>Contact me</h2>

      <div className="card card-content surface">
        {isMessageSent ? (
          <MessageSentOK />
        ) : (
          <>
            <noscript>
              <Prose>
                This form uses <AboutRecaptcha /> to prevent spam, and that
                requires javascript to be enabled. If you prefer, you can
                instead send me an email via <EmailAddress />.
              </Prose>
            </noscript>

            <RemoteContent
              provider={{
                domain: "recaptcha.net",
                description: (
                  <>
                    This form uses <AboutRecaptcha /> to prevent spam. If you
                    prefer not to use that, you can instead send me an email via{" "}
                    <EmailAddress />.
                  </>
                ),
              }}
              content={() => (
                <ContactForm
                  onMessageSent={() => setIsMessageSent(true)}
                  recaptchaPublicSiteKey={props.recaptchaPublicSiteKey}
                />
              )}
            />
          </>
        )}
      </div>
    </Prose>
  );
}

const MessageSentOK = () => {
  return (
    <Prose {...testId(TestTarget.ContactSuccess)}>
      <h2>Thank you</h2>

      <p>
        Your message has been sent successfully. I will get back to you as soon
        as possible.
      </p>
    </Prose>
  );
};

const EmailAddress = () => (
  <>
    <code>michael</code> at this domain name
  </>
);

const AboutRecaptcha = () => (
  <ExternalLink href="https://cloud.google.com/security/products/recaptcha">
    reCAPTCHA by Google
  </ExternalLink>
);

const ContactForm = (
  props: { onMessageSent: () => void } & ContactFormProps,
) => {
  const { onMessageSent } = props;
  const [name, nameProps, nameIsValid] = useRequiredText();
  const [contact, contactProps, contactIsValid] = useRequiredText();
  const [message, messageProps, messageIsValid] = useRequiredText();
  const [captchaToken, setCaptchaToken] = useState<string | undefined>(
    undefined,
  );

  const [error, setError] = useState<string | null>(null);

  const isValid = useMemo(() => {
    return nameIsValid && contactIsValid && messageIsValid && captchaToken;
  }, [nameIsValid, contactIsValid, messageIsValid, captchaToken]);

  const submit = useCallback(() => {
    if (!isValid) {
      setError("Please fill in all the fields and complete the captcha");
      return;
    }
    setError(null);

    client
      .POST("/api/contact/", {
        body: {
          name,
          message,
          contact_info: contact,
          recaptcha_token: captchaToken!,
        },
      })
      .then((response) => {
        if (response.response.ok) {
          onMessageSent();
        } else {
          setError(`Failed to send message: ${response.error}`);
        }
      })
      .catch((e) => {
        setError(`Api error ${e}`);
      });
  }, [captchaToken, onMessageSent, isValid, name, contact, message]);

  return (
    <div>
      <form action={submit} {...testId(TestTarget.ContactForm)}>
        <Prose>
          <FormField
            label="What should I call you?"
            block={(id) => (
              <input
                id={id}
                className={TextInputClassName}
                data-has-error={nameIsValid && !error}
                type="text"
                name="name"
                autoComplete="name"
                placeholder="Your name"
                autoFocus
                required
                {...nameProps}
                {...testId(TestTarget.ContactName)}
              />
            )}
          />

          <FormField
            label="How can I contact you?"
            block={(id) => (
              <input
                id={id}
                className={TextInputClassName}
                data-has-error={contactIsValid && !error}
                name="method"
                type="text"
                autoComplete="email"
                placeholder="Your email address, IM username and service, whatever."
                required
                {...contactProps}
                {...testId(TestTarget.ContactMethod)}
              />
            )}
          />

          <FormField
            label="What would you like to say?"
            block={(id) => (
              <textarea
                id={id}
                className={TextInputClassName}
                data-has-error={messageIsValid && !error}
                name="message"
                autoComplete="off"
                placeholder="Your message"
                rows={5}
                required
                {...messageProps}
                {...testId(TestTarget.ContactMessage)}
              />
            )}
          />
        </Prose>

        <Row className="justify-between items-start">
          <Recaptcha
            recaptchaPublicSiteKey={props.recaptchaPublicSiteKey}
            onSuccess={(token) => {
              setCaptchaToken(token);
              setError(null);
            }}
            onExpired={() => {
              setCaptchaToken(undefined);
              setError(null);
            }}
            onError={() => {
              setCaptchaToken(undefined);
              setError("Captcha error: please try again.");
            }}
          />
          <TintedButton
            type="submit"
            disabled={!isValid}
            title={onlyIf(!isValid, "Fill out the form to enable")}
            className="place-self-end"
          >
            Send
          </TintedButton>
        </Row>

        <div>{error}</div>
      </form>
    </div>
  );
};

const useRequiredText = (): [
  string,
  { value: string; onChange: (ev: ChangeEvent) => void },
  boolean,
] => {
  const [text, setText] = useState("");
  const isValid = useMemo(() => !!text.length, [text]);

  return [
    text,
    {
      value: text,
      onChange: (ev: ChangeEvent) =>
        setText(
          (ev.currentTarget as HTMLInputElement | HTMLTextAreaElement).value,
        ),
    },
    isValid,
  ];
};
