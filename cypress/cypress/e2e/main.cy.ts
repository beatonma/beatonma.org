import { PrivateContentTag } from "./config";

const nextPageButtonQuery = "[title='Next page']";
const lastPageButtonQuery = "[title='Last page']";

describe("Index page displays correctly", () => {
  const indexUrl = "/";

  beforeEach(() => {
    cy.visit(indexUrl);
  });

  it("Displays main widgets", () => {
    cy.get("[title='Home']");
    cy.get("#search");
    cy.get("#github_recent");
    cy.get("#feed");
  });

  it("Feed pagination works", () => {
    cy.get(nextPageButtonQuery).click();
    cy.url().should("include", "?page=2");

    // Github should only be on the first page.
    traversePagination(() => cy.get("#github_recent").should("not.exist"));
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
    cy.get("#search_icon").click();
    cy.get("#search").type("test{enter}");
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
      error.message.includes(nextPageButtonQuery) ||
      error.message.includes(lastPageButtonQuery) ||
      "@button"
    ) {
      // Catch error when next/last page button is not available.
    } else throw error;
  });

  cy.get(`${nextPageButtonQuery}, ${lastPageButtonQuery}`)
    .as("button")
    .then(($button) => {
      if ($button.length !== 0) {
        cy.get("@button").first().click();
        traversePagination(onPageChange);
      }
    });
};
