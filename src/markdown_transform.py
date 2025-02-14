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