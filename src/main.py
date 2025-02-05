from textnode import *
from htmlnode import *

def main():
    node1 = TextNode("dummyvalue", TextType.BOLD, "https://www.boot.dev")
    print(node1)

if __name__ == "__main__":
    main()