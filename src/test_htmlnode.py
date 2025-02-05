import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        x = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        node = HTMLNode('a', 'Test node', '', x)
        HTMLNode.props_to_html(node)

    def test_props_two(self):
        node = HTMLNode('', '', '', '')
        HTMLNode.props_to_html(node)

    def test_props_three(self):
        x = {
                "href": "https://www.twitch.tv",
            }
        node = HTMLNode('', '', '', x)
        HTMLNode.props_to_html(node)        

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