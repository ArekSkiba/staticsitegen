import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )     

    def test_leaf_node(self):
        node1 = LeafNode("p", "Hello")
        self.assertEqual(node1.to_html(), "<p>Hello</p>")

        node2 = LeafNode(None, "Just text")
        self.assertEqual(node2.to_html(), "Just text")

        node3 = LeafNode("a", "Click!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node3.to_html(), '<a href="https://www.google.com" target="_blank">Click!</a>')

        # Test ValueError case
        with self.assertRaises(ValueError):
            bad_node = LeafNode("p", None)
            bad_node.to_html()


if __name__ == "__main__":
    unittest.main()