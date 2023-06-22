import { serverUrl } from "./config.cy";

const url = serverUrl("/contact/");
const contactNameID = "#contact_name";
const contactMethodID = "#contact_method";
const contactMessageID = "#contact_message";
const contactSubmitID = "#contact_submit";

const getInvalidInputs = () => cy.get("input:invalid, textarea:invalid");

const clickRecaptcha = () => {
    cy.get(".g-recaptcha iframe").then(iframe => {
        const body = iframe.contents().find("body");
        cy.wrap(body).find(".recaptcha-checkbox-border").click();
    });
};

describe("Contact page is correct", () => {
    it("Renders correctly", () => {
        cy.visit(url);
        cy.get(contactNameID).should("be.visible");
        cy.get(contactMethodID).should("be.visible");
        cy.get(contactMessageID).should("be.visible");

        cy.get(contactSubmitID).should("not.be.visible");

        clickRecaptcha();

        cy.get(contactSubmitID).should("be.visible");
    });

    it("Validates correctly", () => {
        cy.visit(url);
        clickRecaptcha();

        cy.get(contactSubmitID).click();
        getInvalidInputs().should("have.length", 3);

        cy.get(contactMessageID).type("Sample message");
        cy.get(contactSubmitID).click();
        getInvalidInputs().should("have.length", 2);

        cy.contains("Thank you").should("not.exist");

        cy.get(contactNameID).type("Sample name");
        cy.get(contactMethodID).type("sample@beatonma.org");
        cy.get(contactSubmitID).click();
        getInvalidInputs().should("have.length", 0);

        cy.contains("Thank you");
    });
});
