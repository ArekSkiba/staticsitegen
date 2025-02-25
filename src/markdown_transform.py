from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

def markdown_to_blocks(markdown):
    str_list = markdown.split("\n\n")
    str_clear = [] 
    for str in str_list:
        str_clear.append(str.strip())
    str_filter = filter(None, str_clear)
    return list(str_filter)

def block_to_block_type(block):
    block_type = []
    
    if (len(block.split("\n")) == 1):
        if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            block_type.append("heading")
        elif block[:3] == "```" and block[-3:] == "```":
            block_type.append("code")
        elif block[:2] == "> ":
            block_type.append("quote")
    else:    
        line = block.split("\n")
        n = 0
        if line[0][:3] == "```" and line[-1][-3:] == "```":
            block_type.append("code")
        else:
            for x in line:
                if x[:2] == "> ":
                    block_type.append("quote")
                elif x[:2] == "* " or x[:2] == "- ":
                    block_type.append("unordered_list")
                elif x[0].isdigit() and x[1:3] == ". " and (int(x[0]) == n+1):
                    n = int(x[0])
                    block_type.append("ordered_list")
                else:
                    block_type.append("paragraph")
            block_type = list(dict.fromkeys(block_type))

    if(len(block_type) == 1):
        block_type = block_type[0]
    else:
        block_type = 'paragraph'

    return block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parentnodes = []

    for block in blocks:
        block_type = block_to_block_type(block) 
        match block_type:
            case "paragraph":
                clean_text = paragraph_cleaning(block)
                parentnodes.append(ParentNode("p", text_to_children(clean_text)))
            case "heading":
                h_n = block.count("#")
                clean_text = block.lstrip("#").strip()
                parentnodes.append(ParentNode(f"h{h_n}", text_to_children(clean_text)))
            case "code":
                clean_text = code_cleaning(block)
                parentnodes.append(ParentNode("pre", [ParentNode("code", [clean_text])]))
            case "quote":
                clean_text = quote_cleaning(block)
                parentnodes.append(ParentNode("blockquote", text_to_children(clean_text)))
            case "unordered_list":
                bullet = "* "
                parentnodes.append(ParentNode("ul", list_process(block, bullet)))
            case "ordered_list":
                bullet = ". "
                parentnodes.append(ParentNode("ol", list_process(block, bullet)))
            case _:
                raise ValueError("invalid block type")
                
    return ParentNode("div", parentnodes)
    
def text_to_children(text):
    textnodes = text_to_textnodes(text)
    childnodes = []
    for textnode in textnodes:
        childnode = text_node_to_html_node(textnode)
        childnodes.append(childnode)
    return childnodes

def paragraph_cleaning(paragraph):
    split_text = paragraph.split("\n")
    return " ".join(split_text)

def code_cleaning(code):
    clean = code[3:-3]
    lines = clean.split("\n")
    
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    
    min_indent = None
    for line in lines:
        if line.strip():
            current_indent = len(line) - len(line.lstrip())
            if min_indent is None or current_indent < min_indent:
                min_indent = current_indent
    
    if min_indent:
        lines = [line[min_indent:] if line.strip() else line for line in lines]
    
    return LeafNode(None, "\n".join(lines))

def quote_cleaning(quote):
    split_text = quote.split("\n")
    clean_list = []
    for line in split_text:
        clean_list.append(line.strip(">").strip())
    return " ".join(clean_list)

def list_process(list, bullet):
    split_list = list.split("\n")
    node_list = []
    for line in split_list:
        if bullet == "* ":
            clean_line = line[len(bullet):]
        else: 
            clean_line = line.split(bullet, 1)[1].strip()
        node_list.append(ParentNode("li", text_to_children(clean_line)))
    return node_list

def extract_title(markdown):
    lines = markdown.split("\n")
    result = ""
    for line in lines:
        if line.startswith("# "):
            result = line.lstrip("# ").strip()
            return result
    if not result:
        raise Exception("no h1 line in markdown text")