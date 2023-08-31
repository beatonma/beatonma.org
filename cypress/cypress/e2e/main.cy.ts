import { CyAttr, PrivateContentTag } from "./config";

describe("Index page displays correctly", () => {
  const indexUrl = "/";

  beforeEach(() => {
    cy.visit(indexUrl);
  });

  it("Displays main widgets", () => {
    cy.get(CyAttr.SiteName);
    cy.get(CyAttr.Search);
    cy.get(CyAttr.Github);
    cy.get(CyAttr.Feed);
  });

  it("Feed pagination works", () => {
    cy.get(CyAttr.PageNext).click();
    cy.url().should("include", "?page=2");

    // Github should only be on the first page.
    traversePagination(() => cy.get(CyAttr.Github).should("not.exist"));
  });

  it("No unpublished content is displayed", () => {
    /**
     * If this test fails it implies an issue with the backend - unpublished
     * content should never be available to the frontend.
     */
    const noPrivate = () => cy.contains(PrivateContentTag).should("not.exist");

    traversePagination(noPrivate);
  });

  it("Search UI works", () => {
    cy.get(CyAttr.SearchIcon).click();
    cy.get(CyAttr.Search).type("test{enter}");
    cy.url().should("include", "/search/?query=test");
  });

  it("Displays github feed", () => {
    cy.contains("github/beatonma");
  });
});

const traversePagination = (onPageChange: () => void) => {
  onPageChange();

  Cypress.on("fail", (error, runnable) => {
    if (
      error.message.includes(CyAttr.PageNext) ||
      error.message.includes(CyAttr.PageLast) ||
      "@button"
    ) {
      // Catch error when next/last page button is not available.
    } else {
      throw error;
    }
  });

  cy.get(`${CyAttr.PageNext}, ${CyAttr.PageLast}`)
    .as("button")
    .then(($button) => {
      if ($button.length !== 0) {
        cy.get("@button").first().click();
        traversePagination(onPageChange);
      }
    });
};
