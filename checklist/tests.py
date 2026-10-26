from django.test import TestCase
from django.urls import reverse

from .markdown import render_markdown
from .models import Item, Section


class RenderMarkdownTests(TestCase):
    def test_blank_guidance_renders_as_empty_string(self):
        self.assertEqual(render_markdown(""), "")
        self.assertEqual(render_markdown("   \n  "), "")

    def test_inline_formatting(self):
        self.assertIn("<strong>gain</strong>", render_markdown("Set the **gain**"))

    def test_single_newline_is_a_line_break(self):
        self.assertIn("<br />", render_markdown("one\ntwo"))

    def test_list_may_start_on_the_line_after_a_sentence(self):
        html = render_markdown("Do this:\n- step one\n- step two")
        self.assertIn("<ul>", html)
        self.assertEqual(html.count("<li>"), 2)

    def test_list_items_stay_tight(self):
        # Loosening the list would wrap each <li> in its own <p>.
        html = render_markdown("Do this:\n- step one\n- step two")
        self.assertNotIn("<li><p>", html)

    def test_continuation_line_stays_inside_its_list_item(self):
        html = render_markdown("- step one\n  and more\n- step two")
        self.assertEqual(html.count("<li>"), 2)

    def test_admin_authored_html_passes_through(self):
        html = render_markdown('<img src="https://example.com/rack.jpg">')
        self.assertIn('<img src="https://example.com/rack.jpg">', html)


class ItemGuidanceTests(TestCase):
    def setUp(self):
        self.section = Section.objects.create(title="Audio")

    def test_guidance_html_is_empty_without_guidance(self):
        item = Item.objects.create(section=self.section, text="Mic check")
        self.assertEqual(item.guidance_html, "")

    def test_guidance_html_renders_markdown(self):
        item = Item.objects.create(
            section=self.section, text="Mic check", guidance="Set the **gain**"
        )
        self.assertIn("<strong>gain</strong>", item.guidance_html)


class ChecklistPageTests(TestCase):
    def setUp(self):
        self.section = Section.objects.create(title="Audio")

    def test_item_with_guidance_gets_a_badge_and_a_template(self):
        Item.objects.create(
            section=self.section, text="Ring out the room", guidance="Pull back **6 dB**"
        )
        html = self.client.get(reverse("checklist")).content.decode()
        self.assertIn("has-guidance", html)
        self.assertIn("data-guidance-open", html)
        self.assertIn("<template data-guidance>", html)
        self.assertIn("<strong>6 dB</strong>", html)

    def test_item_without_guidance_has_no_badge(self):
        Item.objects.create(section=self.section, text="Mic check")
        html = self.client.get(reverse("checklist")).content.decode()
        self.assertNotIn("has-guidance", html)
        self.assertNotIn("data-guidance-open", html)

    def test_item_text_is_still_escaped(self):
        Item.objects.create(section=self.section, text="Check <b>everything</b>")
        html = self.client.get(reverse("checklist")).content.decode()
        self.assertIn("Check &lt;b&gt;everything&lt;/b&gt;", html)
