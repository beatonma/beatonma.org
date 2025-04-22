from basetest.testcase import SimpleTestCase
from main.models.posts.formats import Formats


class FormatsTest(SimpleTestCase):
    def test_callout(self):
        markdown = """> [!WARNING]
> `python manage.py migrate` required for new fields.  

- Added `has_been_read: bool` field.  """

        html = """<div class="template-callout-warn"><p><strong>Warning</strong></p><p><code>python manage.py 
migrate</code> required for new fields.</p></div>
<ul><li>Added <code>has_been_read: bool</code> field.</li></ul>
"""

        print(Formats.to_html(Formats.MARKDOWN, markdown))
        self.assertHTMLEqual(Formats.to_html(Formats.MARKDOWN, markdown), html)
