import { serverUrl } from "./config.cy";

describe("About page displays correctly", () => {
    const url = serverUrl("/about/");
    it("Renders correctly", () => {
        cy.visit(url);
        cy.title().should("contain", "About");
        cy.contains("beatonma.org");
        cy.get("article").should("be.visible");
    });

    it("Displays hcard", () => {
        cy.visit(url);
        cy.get(".h-card").should("be.visible");
        cy.contains("Michael Beaton");
    });
});
