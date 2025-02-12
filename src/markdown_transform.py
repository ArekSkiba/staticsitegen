def markdown_to_blocks(markdown):
    str_list = markdown.split("\n\n")
    str_clear = [] 
    for str in str_list:
        str_clear.append(str.strip())
    str_filter = filter(None, str_clear)
    return list(str_filter)