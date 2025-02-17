import unittest

from markdown_transform import markdown_to_blocks, block_to_block_type, markdown_to_html_node


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

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
* This is a list
* with items
* and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_basic_code_block(self):
        md = """```
    def hello():
        print('hello')
    ```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>def hello():\n    print('hello')</code></pre></div>"
        )

    def test_indented_code_block(self):
        md = """```
        def hello():
            print('hello')
        ```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>def hello():\n    print('hello')</code></pre></div>"
        )

    def test_empty_code_block(self):
        md = """```
    ```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code></code></pre></div>"
        )

if __name__ == "__main__":
    unittest.main()