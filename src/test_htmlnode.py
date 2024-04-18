import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_node_value(self):
        node = HTMLNode("h1", "Test String", [], {})
        self.assertEqual(str(node), "<h1>Test String</h1>")

    def test_node_children(self):
        p1 = HTMLNode("p", "Test 1", [], {})
        p2 = HTMLNode("p", "Test 2", [], {})
        node = HTMLNode("div", None, [p1, p2], {})
        self.assertEqual(str(node), "<div><p>Test 1</p><p>Test 2</p></div>")

    def test_node_props(self):
        node = HTMLNode("a", "Test Link", [], {"href": "http://boot.dev"})
        self.assertEqual(str(node), "<a href=\"http://boot.dev\">Test Link</a>")

    def test_leaf_value(self):
        node = LeafNode("h2", "Test String", {})
        self.assertEqual(node.to_html(), "<h2>Test String</h2>")

    def test_leaf_props(self):
        node = LeafNode("a", "Test Link", {"href": "http://boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"http://boot.dev\">Test Link</a>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Test String", {})
        self.assertEqual(node.to_html(), "Test String")

    def test_parent_node(self):
        node = node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()
