import { CyAttr } from "./config";

const getInvalidInputs = () => cy.get("input:invalid, textarea:invalid");

const clickRecaptcha = () => {
  cy.get(".g-recaptcha iframe").then((iframe) => {
    const body = iframe.contents().find("body");
    cy.wrap(body).find(".recaptcha-checkbox-border").click();
  });
};

describe("Contact page is correct", () => {
  const url = "/contact/";
  const contactName = CyAttr.ContactName;
  const contactMethod = CyAttr.ContactMethod;
  const contactMessage = CyAttr.ContactMessage;
  const contactSubmit = CyAttr.ContactSubmit;

  beforeEach(() => cy.visit(url));

  it("Renders correctly", () => {
    cy.get(contactName).should("be.visible");
    cy.get(contactMethod).should("be.visible");
    cy.get(contactMessage).should("be.visible");

    cy.get(contactSubmit).should("not.be.enabled");

    clickRecaptcha();

    cy.get(contactSubmit).should("be.enabled");
  });

  it("Validates correctly", () => {
    clickRecaptcha();

    cy.get(contactSubmit).click();
    getInvalidInputs().should("have.length", 3);

    cy.get(contactMessage).type("Sample message");
    cy.get(contactSubmit).click();
    getInvalidInputs().should("have.length", 2);

    cy.contains("Thank you").should("not.exist");

    cy.get(contactName).type("Sample name");
    cy.get(contactMethod).type("sample@beatonma.org");
    cy.get(contactSubmit).click();
    getInvalidInputs().should("have.length", 0);

    cy.get(CyAttr.ContactSuccess).should("be.visible");
    cy.contains("Thank you");
  });
});
