import { CyAttr } from "./config";

describe("About page displays correctly", () => {
  const url = "/about/";

  beforeEach(() => cy.visit(url));

  it("Renders correctly", () => {
    cy.title().should("contain", "About");
    cy.get(CyAttr.AboutMe).should("be.visible");
  });

  it("Displays hcard", () => {
    cy.get(".h-card").should("be.visible").contains("Michael Beaton");
  });
});
