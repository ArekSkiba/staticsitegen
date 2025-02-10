import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
            
        if node.text.count(delimiter) % 2 != 0:
            raise Exception('Number of delimiters is not equal, the syntax is invalid.')

        text_split = node.text.split(delimiter)

        for i, line in enumerate(text_split):
            if line == "":
                continue
            if i % 2 != 0:
                x = TextNode(line, text_type)
                result.append(x)
            else:
                x = TextNode(line, TextType.TEXT)
                result.append(x)
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if len(extract_markdown_images(node.text)) == 0:
            result.append(node)
            continue
        link_list = extract_markdown_images(node.text)
        original_text = node.text

        for text,link in link_list:
            sections = original_text.split(f"![{text}]({link})", 1)
            if sections[0]:
                x = TextNode(sections[0], TextType.TEXT)
                result.append(x)
            if text:
                c = TextNode(text, TextType.IMAGE, link)
                result.append(c)
            original_text = sections[1]
        if original_text:
            z = TextNode(original_text, TextType.TEXT)
            result.append(z)
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if len(extract_markdown_links(node.text)) == 0:
            result.append(node)
            continue
        link_list = extract_markdown_links(node.text)
        original_text = node.text

        for text,link in link_list:
            sections = original_text.split(f"[{text}]({link})", 1)
            if sections[0]:
                x = TextNode(sections[0], TextType.TEXT)
                result.append(x)
            if text:
                c = TextNode(text, TextType.LINK, link)
                result.append(c)
            original_text = sections[1]
        if original_text:
            z = TextNode(original_text, TextType.TEXT)
            result.append(z)
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes