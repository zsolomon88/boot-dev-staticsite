import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_html_text(self):
        node = TextNode("Test node text", "text")
        html_leaf = text_node_to_html_node(node)
        self.assertEqual(html_leaf.to_html(), "Test node text")
    
    def test_html_bold(self):
        node = TextNode("Test node text", "bold")
        html_leaf = text_node_to_html_node(node)
        self.assertEqual(html_leaf.to_html(), "<b>Test node text</b>")

    def test_html_italic(self):
        node = TextNode("Test node text", "italic")
        html_leaf = text_node_to_html_node(node)
        self.assertEqual(html_leaf.to_html(), "<i>Test node text</i>")

    def test_html_code(self):
        node = TextNode("Test node text", "code")
        html_leaf = text_node_to_html_node(node)
        self.assertEqual(html_leaf.to_html(), "<code>Test node text</code>")

    def test_html_link(self):
        node = TextNode("Test node text", "link", "http://www.boot.dev")
        html_leaf = text_node_to_html_node(node)
        self.assertEqual(html_leaf.to_html(), "<a href=\"http://www.boot.dev\">Test node text</a>")

    def test_html_img(self):
        node = TextNode("Test node text", "image", "http://www.boot.dev")
        html_leaf = text_node_to_html_node(node)
        self.assertEqual(html_leaf.to_html(), "<img src=\"http://www.boot.dev\" alt=\"Test node text\" />")

    def test_simple_split(self):
        node = [TextNode("Test *node* text", "text")]
        split_nodes = split_nodes_delimiter(node, "*", "bold")
        self.assertEqual(split_nodes, [TextNode("Test ", "text"), TextNode("node", "bold"), TextNode(" text", "text")])

    def test_double_split(self):
        node = [TextNode("Test `node` text `node` test", "text")]
        split_nodes = split_nodes_delimiter(node, "`", "code")
        self.assertEqual(split_nodes, [TextNode("Test ", "text"), TextNode("node", "code"), TextNode(" text ", "text"), TextNode("node", "code"), TextNode(" test", "text")])

    def test_image_extraction(self):
        image_list = extract_markdown_images("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)")
        self.assertEqual(image_list, [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_link_extraction(self):
        link_list = extract_markdown_links("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)")
        self.assertEqual(link_list, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_image_split(self):
        node = [TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",text_type_text)]
        new_nodes = split_nodes_image(node)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]
)

if __name__ == "__main__":
    unittest.main()
