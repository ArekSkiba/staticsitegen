import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()