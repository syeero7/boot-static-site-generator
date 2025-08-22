class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_str = ""
        if not self.props:
            return props_str
        for key in self.props:
            props_str += f'{key}="{self.props[key]}" '
        return props_str.strip()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError(f"value is missing: {self.value}")
        if not self.tag:
            return self.value
        attributes = self.props_to_html()
        if len(attributes) > 0:
            attributes = f" {attributes}"
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
