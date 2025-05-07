import { RepresentativeUrls, toFilename } from "./config";

describe("Visit a sample page for each type of content", () => {
  it("Record a screenshot of each page", () => {
    const dirname = new Date().toISOString().slice(0, 10);
    RepresentativeUrls.forEach((url) => {
      const targetFilename = `${dirname}/${toFilename(url)}`;
      cy.visit(url);
      cy.screenshot(targetFilename, { overwrite: true, timeout: 5_000 });
    });
  });
});
