from textnode import *
from htmlnode import *
import shutil
import os

static_path = './static'
public_path = './public'


def main():
    if not os.path.exists(static_path):
        raise Exception('source directory does not exist')
    if os.path.exists(public_path):
        shutil.rmtree(public_path) 
    os.mkdir(public_path)
    copy_contents(static_path, public_path)
    
    
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





if __name__ == "__main__":
    main()