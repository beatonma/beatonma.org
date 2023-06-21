import { serverUrl } from "./config.cy";

describe("Index page displays correctly", () => {
    const indexUrl = serverUrl("/");

    it("Opens the main page", () => {
        cy.visit(indexUrl);
        cy.contains("beatonma.org");

        cy.get("#github_recent");
        cy.get("#feed");
    });

    it("Feed pagination works", () => {
        cy.visit(indexUrl);
        cy.get("[title='Next page']").click();
        cy.url().should("include", "?page=2");

        // Github and notes should only be on the first page.
        cy.get("#github_recent").should("not.exist");
    });

    it("Search UI works", () => {
        cy.visit(indexUrl);
        cy.get("#search_icon").click();
        cy.get("#search").type("test{enter}");
        cy.url().should("include", "/search/?query=test");
    });

    it("Displays github feed", () => {
        cy.visit(indexUrl);
        cy.contains("github/beatonma");
    });
});
