import { ExportForTesting } from "./build-templates";
import { describe, test, expect } from "@jest/globals";
import { measurePerformance } from "core/util";

const { WhitespacePatterns, minimiseWhitespace } = ExportForTesting;

const expectNoChanges = <T extends any>(transform: (v: T) => T, value: T) =>
    expect(transform(value)).toBe(value);

describe("Templates", () => {
    describe("minimiseWhitespace", () => {
        test("afterDjangoTag", () => {
            expect(
                minimiseWhitespace(
                    `{% block footer %}\n{% include "./_footer.html" %}\n{% endblock %}`,
                ),
            ).toBe(
                `{% block footer %}{% include "./_footer.html" %}{% endblock %}`,
            );
        });

        test("inHtmlTag", () => {
            expect(
                minimiseWhitespace(`<a  href="#"\ntitle="blah"\n>section</a>`),
            ).toBe(`<a href="#" title="blah">section</a>`);
        });

        test("html + django tag collisions", () => {
            // Make sure <> characters used within Django tags or string literals
            // do not get treated as HTML tag boundaries.
            const data = `<div class="pagination-group" data-testtag="{% if 2 < 1 %}{% endif %}">
                    {% if page_obj.has_previous %}
                      <a href="/#content" title="First page" class="tooltip">
                          <span class="icon">first_page</span>
                      </a>
    
                      {% if page_obj.number > 2 %}
                        <a href="?page={{ page_obj.previous_page_number }}#content" title="Previous page" class="tooltip">
                            <span class="icon">navigate_before</span>
                        </a>
                      {% endif %}
                    {% endif %}
                </div>`;

            const expected = `<div class="pagination-group" data-testtag="{% if 2 < 1 %}{% endif %}">
{% if page_obj.has_previous %}<a href="/#content" title="First page" class="tooltip">
<span class="icon">first_page</span>
</a>
{% if page_obj.number > 2 %}<a href="?page={{ page_obj.previous_page_number }}#content" title="Previous page" class="tooltip">
<span class="icon">navigate_before</span>
</a>
{% endif %}{% endif %}</div>`;

            expect(minimiseWhitespace(data)).toBe(expected);
        });

        test("performance", () => {
            measurePerformance(() => {
                minimiseWhitespace(`<a  href="#"\ntitle="blah"\n>section</a>`);
            }, 100);
        });

        test("complete", () => {
            const data = `<head>
    <title >{% block title %}{% endblock %}
      {% block title_suffix %} - __env__:siteName{% endblock %}
    </title>
    <meta name="description" content="{% block description %}Things by Michael Beaton{% endblock %}" />
    {% include "./_head.html" %}
    {% block html_head %}{% endblock %}
</head>`;

            const expected = `<head>
<title>{% block title %}{% endblock %}{% block title_suffix %} - __env__:siteName{% endblock %}</title>
<meta name="description" content="{% block description %}Things by Michael Beaton{% endblock %}" />
{% include "./_head.html" %}{% block html_head %}{% endblock %}</head>`;

            expect(minimiseWhitespace(data)).toBe(expected);
        });
    });

    describe("Whitespace patterns", () => {
        test("lineBreaksInHtmlTag", () => {
            const transform = (str: string) =>
                str.replace(WhitespacePatterns.lineBreaksInHtmlTag, " ");

            expect(
                transform(`<a  href="#"\ntitle="blah"\n\r\r\r\n>section</a>`),
            ).toEqual(`<a  href="#" title="blah" >section</a>`);

            expect(
                transform(
                    `<div\nclass="wrapper"><pre>multiline\ncontent\nunchanged</pre></div>`,
                ),
            ).toBe(
                `<div class="wrapper"><pre>multiline\ncontent\nunchanged</pre></div>`,
            );

            expectNoChanges(
                transform,
                `<div class="cls">\n<div class="cls">\n</div></div>`,
            );

            expectNoChanges(
                transform,
                `<div class="pagination-group">
                    {% if page_obj.has_previous %}
                      <a href="/#content" title="First page" class="tooltip">
                          <span class="icon">first_page</span>
                      </a>

                      {% if page_obj.number > 2 %}
                        <a href="?page={{ page_obj.previous_page_number }}#content" title="Previous page" class="tooltip">
                            <span class="icon">navigate_before</span>
                        </a>
                      {% endif %}
                    {% endif %}
                </div>`,
            );
        });

        test("endOfHtmlTag", () => {
            const transform = (str: string) =>
                str.replace(WhitespacePatterns.endOfHtmlTag, "");

            expect(transform(`<a  href="#"\ntitle="blah"  >section</a>`)).toBe(
                `<a  href="#"\ntitle="blah">section</a>`,
            );

            expect(transform(`<a  href="#"\ntitle="blah" />`)).toBe(
                `<a  href="#"\ntitle="blah"/>`,
            );

            // '>' character used as operator in embedded Django tag.
            expectNoChanges(transform, `{% if page_obj.number > 2 %}`);

            expectNoChanges(
                transform,
                `<div>\n{% if page_obj.number > 2 %}\n</div>`,
            );
        });

        test("atLineStart", () => {
            const transform = (str: string) =>
                str.replace(WhitespacePatterns.atLineStart, "");

            expect(transform(`   indented  content\n     again`)).toBe(
                "indented  content\nagain",
            );
        });

        test("repeatedSpaces", () => {
            const transform = (str: string) =>
                str.replace(WhitespacePatterns.repeatedSpaces, "");

            expect(transform("  a simple   _test   ")).toBe("a simple_test");
        });

        test("linebreaks", () => {
            const transform = (str: string) =>
                str.replace(WhitespacePatterns.linebreaks, "\n");

            expect(transform(`  a\n  simple  \r\n  _test `)).toBe(
                `  a\nsimple\n_test `,
            );
        });

        test("repeatedSpaces", () => {
            const transform = (str: string) =>
                str.replace(WhitespacePatterns.repeatedSpaces, " ");

            expect(transform(" 1  2   3 ")).toBe(" 1 2 3 ");
        });
    });
});
