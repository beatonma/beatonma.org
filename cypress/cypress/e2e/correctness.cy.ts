import { RepresentativeUrls, toFilename } from "./config";

describe("Visit a sample page for each type of content", () => {
  it("No .canary or TODO  markers found on any pages", () => {
    RepresentativeUrls.forEach((url) => {
      cy.visit(url);
      cy.contains("todo", { matchCase: false }).should("not.exist");
      cy.get(".canary").should("not.exist");
    });
  });

  it("Record a screenshot of each page", () => {
    const dirname = new Date().toISOString().slice(0, 10);
    RepresentativeUrls.forEach((url) => {
      const targetFilename = `${dirname}/${toFilename(url)}`;
      cy.visit(url);
      cy.screenshot(targetFilename, { overwrite: true });
    });
  });
});
