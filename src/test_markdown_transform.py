import unittest

from markdown_transform import markdown_to_blocks, block_to_block_type


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown_string = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        result = markdown_to_blocks(markdown_string)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ],
            result,
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_heading(self):
        markdown_block = "# This is a heading"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, "heading")

    def test_block_to_block_code(self):
        markdown_block = "```This is \na code```"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, "code")

    def test_block_to_block_quote(self):
        markdown_block = "> first line\n> second line"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, "quote")

    def test_block_to_block_ulist(self):
        markdown_block = "* This is unordered list\n* second bullet"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, "unordered_list")

    def test_block_to_block_olist(self):
        markdown_block = "1. This is ordered list\n2. second bullet"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, "ordered_list")
    
    def test_block_to_block_paragraph(self):
        markdown_block = "3. This is ordered list2. second bullet"
        result = block_to_block_type(markdown_block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

if __name__ == "__main__":
    unittest.main()