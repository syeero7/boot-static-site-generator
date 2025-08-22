import unittest

from htmlnode import HTMLNode, LeafNode


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
