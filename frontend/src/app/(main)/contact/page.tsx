import { Metadata } from "next";
import { ContactPage } from "./contact-form";

export const metadata: Metadata = {
  title: "Contact me",
  description: "Send me a message",
};

export default async function Page() {
  return (
    <ContactPage
      recaptchaPublicSiteKey={process.env.NEXT_PUBLIC_GOOGLE_RECAPTCHA_TOKEN!}
    />
  );
}
