import { Navigation } from "./config";

describe("About page displays correctly", () => {
  beforeEach(() => cy.visit(Navigation.about()));

  it("Displays hcard", () => {
    cy.get(".h-card").should("be.visible").contains("Firstname Surname");
  });

  it("Shows content", () => {
    cy.get("body").contains("TestTarget about content");
  });
});
