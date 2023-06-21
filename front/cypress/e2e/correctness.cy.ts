import { formatDateISO } from "../../src/apps/main/js/util/datetime";
import { RepresentativeUrls, toFilename } from "./config.cy";

describe("Visit a sample page for each type of content", () => {
    it("Check no TODO markers left on any templates", () => {
        RepresentativeUrls.forEach(url => {
            cy.visit(url);
            cy.contains("todo", { matchCase: false }).should("not.exist");
        });
    });

    it("Record a screenshot of each page", () => {
        const date = new Date();
        const dirname = formatDateISO(date);
        RepresentativeUrls.forEach(url => {
            const targetFilename = `${dirname}/${toFilename(url)}`;
            cy.visit(url);
            cy.screenshot(targetFilename, { overwrite: true });
        });
    });
});
