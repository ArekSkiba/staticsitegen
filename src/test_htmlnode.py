import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_parent(self):
        # Test standard case with tag and children list
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node1.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

        # Test valid case: children is an empty list
        node_with_no_children = ParentNode("i", [])
        self.assertEqual(node_with_no_children.to_html(), "<i></i>")

        # Test recursive structure with ParentNode inside ParentNode
        nested_node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Item 1"),
                        LeafNode("li", "Item 2")
                    ]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Some paragraph text.")
                    ]
                )
            ]
        )
        self.assertEqual(
            nested_node.to_html(),
            "<div><ul><li>Item 1</li><li>Item 2</li></ul><p>Some paragraph text.</p></div>"
        )


        # Test ValueError case for missing tag
        with self.assertRaises(ValueError) as context1:
            bad_node1 = ParentNode(None, [LeafNode(None, "Normal text")])
            bad_node1.to_html()  
        # Optionally check the exact error message
        self.assertEqual(str(context1.exception), "invalid HTML: no tag")

        # Test ValueError case for no children provided
        with self.assertRaises(ValueError) as context2:
            bad_node2 = ParentNode("i", None)
            bad_node2.to_html()
        # Optionally check the exact error message
        self.assertEqual(str(context2.exception), "invalid HTML: no children")    

if __name__ == "__main__":
    unittest.main()