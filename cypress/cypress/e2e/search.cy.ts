import { Navigation, PrivateContentTag } from "./config";

describe("Search results are correct", () => {
  it("Search results are displayed", () => {
    cy.visit(Navigation.search("target"));
    cy.contains("TestTarget Article");
    cy.contains("TestTarget Blog");
    cy.contains("TestTarget App");
    cy.contains("TestTarget Note");
    cy.contains("1.0-TestTarget");
    cy.contains(PrivateContentTag).should("not.exist");
  });

  it("Search results do not show unpublished content", () => {
    /**
     * If this test fails it implies an issue with the backend - unpublished
     * content should never be available to the frontend.
     */
    cy.visit(Navigation.search("PRIVATE"));
    cy.contains(PrivateContentTag).should("not.exist");
  });

  it("Tag results are displayed", () => {
    cy.visit(Navigation.searchTag("sample-tag"));
    cy.title().should("contain", "#sample-tag");
    cy.contains("TestTarget Article");
  });
});
