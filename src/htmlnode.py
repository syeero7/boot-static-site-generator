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
            props_str += f' {key}="{self.props[key]}"'
        return props_str

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
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"value is missing: {self.value}")
        if not self.children:
            raise ValueError(f"children is missing: {self.children}")
        children_str = ""
        for node in self.children:
            children_str += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"
