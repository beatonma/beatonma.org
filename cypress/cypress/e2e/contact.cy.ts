import { Navigation, TestTarget } from "./config";

const getInvalidInputs = () => cy.get("input:invalid, textarea:invalid");

const clickRecaptcha = () => {
  cy.get(`${TestTarget.RecaptchaWrapper} iframe`)
    .first()
    .its("0.contentDocument.body")
    .should("not.be.undefined")
    .and("not.be.empty")
    .then(cy.wrap)
    .find(".recaptcha-checkbox-border")
    .should("be.visible")
    .click();
};

const clickAllowRemoteContent = () =>
  cy.get(TestTarget.AllowRemoteContent).click();

const url = Navigation.contact();
const Target = {
  ...TestTarget.Contact,
  SubmitButton: `${TestTarget.Contact.Form} button`,
};

describe("Contact page is correct", () => {
  beforeEach(() => {
    cy.visit(url);
  });

  it("Shows remote content warning", () => {
    cy.get(TestTarget.AllowRemoteContent).should("be.visible");
  });

  it("Renders correctly", () => {
    clickAllowRemoteContent();
    cy.get(Target.Name).should("be.visible");
    cy.get(Target.Method).should("be.visible");
    cy.get(Target.Message).should("be.visible");
    cy.get(Target.SubmitButton).should("not.be.enabled");
  });

  it("Validates correctly", () => {
    clickAllowRemoteContent();

    cy.get(Target.SubmitButton).click({ force: true }); // Click :disabled button
    getInvalidInputs().should("have.length", 3);

    cy.get(Target.Name).type("name");
    cy.get(Target.Method).type("test@beatonma.org");
    cy.get(Target.Message).type("message");

    cy.get(Target.SubmitButton).click({ force: true });
    getInvalidInputs().should("have.length", 0);

    clickRecaptcha();

    cy.get(Target.SubmitButton).click();
    cy.get(Target.Success, { timeout: 10_000 }).should("be.visible");
  });
});
