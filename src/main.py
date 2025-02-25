from textnode import *
from htmlnode import *
from markdown_transform import markdown_to_html_node, extract_title
import shutil
import os

static_path = './static'
public_path = './public'
content_path = './content'
template_path = './template.html'
output_path = './public'


def main():
    if not os.path.exists(static_path):
        raise Exception('source directory does not exist')
    if os.path.exists(public_path):
        shutil.rmtree(public_path) 
    os.mkdir(public_path)
    copy_contents(static_path, public_path)

    generate_pages_recursive(content_path, template_path, output_path)
    
    
def copy_contents(src_dir, dst_dir):
    
    elements = os.listdir(src_dir)
    if elements:
        for element in elements:
            path = os.path.join(src_dir, element)
            if os.path.isfile(path):
                shutil.copy(path, dst_dir)
            else:
                new_src = os.path.join(src_dir, element)
                new_dst = os.path.join(dst_dir, element) 
                os.mkdir(new_dst)
                copy_contents(new_src, new_dst)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = open(from_path).read()
    template = open(template_path).read()

    root_node = markdown_to_html_node(markdown)
    html_content = root_node.to_html()
    page_title = extract_title(markdown)
    
    output = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)

    directory = os.path.dirname(dest_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    new_html_file = open(dest_path, "w")
    new_html_file.write(output)
    new_html_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
   
    elements = os.listdir(dir_path_content)
    if elements:
        for element in elements:
            if element.endswith('.md'):
                path = os.path.join(dir_path_content, element)
                dest_path = os.path.join(dest_dir_path, element.replace(".md",".html"))
                if os.path.isfile(path):
                    markdown = open(path).read()
                    template = open(template_path).read()

                    root_node = markdown_to_html_node(markdown)
                    html_content = root_node.to_html()
                    page_title = extract_title(markdown)

                    output = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)

                    directory = os.path.dirname(dest_path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    new_html_file = open(dest_path, "w")
                    new_html_file.write(output)
                    new_html_file.close()
            else:
                new_content_path = os.path.join(dir_path_content, element)
                new_dest_path = os.path.join(dest_dir_path, element) 
                os.mkdir(new_dest_path)
                generate_pages_recursive(new_content_path, template_path, new_dest_path)

if __name__ == "__main__":#
    main()