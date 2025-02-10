import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_equrl(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee2")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        # Test TEXT type
        node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "", "Text node should have empty tag")
        self.assertEqual(html_node.value, "Hello, world!", "Text node value should match input text")
        self.assertIsNone(html_node.props, "Text node should have None props")

        # Test BOLD type
        node2 = TextNode("Hello, world!", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b", "Bold node should have b tag")
        self.assertEqual(html_node2.value, "Hello, world!", "Bold node value should be raw text")
        self.assertIsNone(html_node2.props, "Bold node should have None props")
        # Test the rendered HTML
        self.assertEqual(html_node2.to_html(), "<b>Hello, world!</b>", "Bold node should render with bold tags")

        # Test ITALIC type
        node3 = TextNode("Hello, world!", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "i", "Italic node should have i tag")
        self.assertEqual(html_node3.value, "Hello, world!", "Italic node value should be raw text")
        self.assertIsNone(html_node3.props, "Italic node should have None props")
        # Test the rendered HTML
        self.assertEqual(html_node3.to_html(), "<i>Hello, world!</i>", "Italic node should render with i tags")

        # Test CODE type
        node4 = TextNode("Hello, world!", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.tag, "code", "Code node should have code tag")
        self.assertEqual(html_node4.value, "Hello, world!", "Code node value should be raw text")
        self.assertIsNone(html_node4.props, "Code node should have None props")
        # Test the rendered HTML
        self.assertEqual(html_node4.to_html(), "<code>Hello, world!</code>", "Code node should render with code tags")

        # Test LINK type
        node5 = TextNode("click me", TextType.LINK, "https://www.boot.dev/lessons")
        html_node5 = text_node_to_html_node(node5)
        self.assertEqual(html_node5.tag, "a", "Link node should have a tag")
        self.assertEqual(html_node5.value, "click me", "Link node value should be raw text")
        self.assertEqual(html_node5.props, {"href": "https://www.boot.dev/lessons"}, "Link node should have href prop")
        # Test the rendered HTML
        self.assertEqual(html_node5.to_html(), '<a href="https://www.boot.dev/lessons">click me</a>', 'Link node should render with link tags and props as href=link')

        # Test IMG type
        node6 = TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/lessons")
        html_node6 = text_node_to_html_node(node6)
        self.assertEqual(html_node6.tag, "img", "Image node should have a tag")
        self.assertEqual(html_node6.value, "", "Image node text value should be empty string")
        self.assertEqual(html_node6.props, {"src": "https://www.boot.dev/lessons", "alt": "alt text"}, "Image node should have prop with link and alt text")
        # Test the rendered HTML
        self.assertEqual(html_node6.to_html(), '<img src="https://www.boot.dev/lessons" alt="alt text"></img>', 'Image node should render as image with link and alt text as props')

        # Test unknown type
        node7 = TextNode("Hello, world!", "UNKNOWN_TYPE")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node7)
        self.assertTrue("unknown text type" in str(context.exception).lower())

if __name__ == "__main__":
    unittest.main()