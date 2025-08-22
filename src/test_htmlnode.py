import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        node.props = {
            "href": "https://www.github.com",
            "target": "_blank",
        }

        text = 'href="https://www.github.com" target="_blank"'
        self.assertEqual(node.props_to_html(), text)

    def test_not_implementation_err(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_data(self):
        node = HTMLNode("p", "hello world", None, {"class": "text-sm"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world")
        self.assertIsNone(node.children)
        self.assertEqual(node.props_to_html(), 'class="text-sm"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("p", "Hello, world!", {"class": "text-sm"})
        self.assertEqual(node.to_html(), '<p class="text-sm">Hello, world!</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
