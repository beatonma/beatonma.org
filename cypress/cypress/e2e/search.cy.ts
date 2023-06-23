const expectFeedItems = (n: number) => {
    cy.get("#feed").find(".h-entry").should("have.length", n);
};

describe("Search results are correct", () => {
    it("Search results are displayed", () => {
        cy.visit("/search/?query=target");
        cy.contains("TestTarget Article");
        cy.contains("TestTarget Blog");
        cy.contains("TestTarget Repo");
        cy.contains("TestTarget App");
        cy.contains("TestTarget Note");
        cy.contains("1.0-TestTarget");
        cy.contains("__PRIVATE__").should("not.exist");
    });

    it("Search result links are correct", () => {
        cy.visit("/search/?query=target");
        cy.contains("TestTarget Article").click();
        cy.url().should("include", "testtarget-article/");
    });

    it("Language results are displayed", () => {
        cy.visit("/language/testTarget-language/");
        cy.title().should("contain", "TestTarget-Language");
        cy.contains("TestTarget App");
    });

    it("Tag results are displayed", () => {
        cy.visit("/tag/sample-tag/");
        cy.title().should("contain", "#sample-tag");
        cy.contains("TestTarget Article");
    });
});
