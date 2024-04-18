from htmlnode import LeafNode, HTMLNode
import re

text_type_text="text"
text_type_bold="bold"
text_type_italic="italic"
text_type_code="code"
text_type_link="link"
text_type_image="image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"



def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            split_nodes = []
            split_strings = node.text.split(delimiter)
            if len(split_strings) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            
            for i in range(len(split_strings)):
                if split_strings[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(split_strings[i], text_type_text))
                else:
                    split_nodes.append(TextNode(split_strings[i], text_type))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            images_list = extract_markdown_images(node.text)
            split_nodes = []
            if len(images_list) == 0:
                new_nodes.append(node)
                continue
            full_text = node.text
            for image in images_list:
                split_text = full_text.split(f"![{image[0]}]({image[1]})", 1)
                if split_text[0] != "":
                    split_nodes.append(TextNode(split_text[0], text_type_text))
                split_nodes.append(TextNode(image[0], text_type_image, image[1]))
                full_text = split_text[1]
            if full_text != "":
                split_nodes.append(TextNode(full_text, text_type_text))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            links_list = extract_markdown_links(node.text)
            split_nodes = []
            if len(links_list) == 0:
                new_nodes.append(node)
                continue
            full_text = node.text
            for link in links_list:
                split_text = full_text.split(f"[{link[0]}]({link[1]})", 1)
                if split_text[0] != "":
                    split_nodes.append(TextNode(split_text[0], text_type_text))
                split_nodes.append(TextNode(link[0], text_type_link, link[1]))
                full_text = split_text[1]
            if full_text != "":
                split_nodes.append(TextNode(full_text, text_type_text))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):
    nodes_list = []
    #find bolds
    original_node = TextNode(text, text_type_text)
    nodes_list = split_nodes_delimiter([original_node], "**", text_type_bold)

    #now italics
    nodes_list = split_nodes_delimiter(nodes_list, "*", text_type_italic)

    #next code 
    nodes_list = split_nodes_delimiter(nodes_list, "`", text_type_code)

    #then images
    nodes_list = split_nodes_image(nodes_list)
    
    #lastly links
    nodes_list = split_nodes_link(nodes_list)

    return nodes_list