import { TestTarget, Navigation } from "./config";

describe("Index page displays correctly", () => {
  const indexUrl = Navigation.home();

  beforeEach(() => {
    cy.visit(indexUrl);
  });

  it("Displays main widgets", () => {
    cy.get("h1").contains(Cypress.env("NEXT_PUBLIC_SITE_NAME"));
    cy.get(TestTarget.Search.Button);
  });

  it("Search UI works", () => {
    cy.get(TestTarget.Search.Button).click();
    cy.get(TestTarget.Search.Input).type("test{enter}");
    cy.url().should("include", Navigation.search("test"));
  });

  it("Displays github feed", () => {
    cy.contains(`github/${Cypress.env("NEXT_PUBLIC_GITHUB_USERNAME")}`);
  });
});
