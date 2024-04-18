from htmlnode import LeafNode, HTMLNode

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
        if text_node.text_type == "text":
            return LeafNode(None, text_node.text)
        if text_node.text_type == "bold":
            return LeafNode("b", text_node.text)
        if text_node.text_type == "italic":
            return LeafNode("i", text_node.text)
        if text_node.text_type == "code":
            return LeafNode("code", text_node.text)
        if text_node.text_type == "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == "image":
            return LeafNode("img", None, {"alt": text_node.text, "src": text_node.url})
        raise Exception("Invalid text type")