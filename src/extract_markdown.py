import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            nodes.append(node)
            continue
        tmp_txt = node.text
        for i in range(len(matches)):
            alt, src = matches[i][0], matches[i][1]
            splitted = tmp_txt.split(f"![{alt}]({src})", 1)
            if len(splitted[0]) != 0:
                nodes.append(TextNode(splitted[0], TextType.TEXT))
            nodes.append(TextNode(alt, TextType.IMAGE, src))
            if len(splitted[1]) == 0:
                continue
            if len(matches) > i + 1:
                tmp_txt = splitted[1]
            else:
                nodes.append(TextNode(splitted[1], TextType.TEXT))
    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            nodes.append(node)
            continue
        tmp_txt = node.text
        for i in range(len(matches)):
            link_txt, href = matches[i][0], matches[i][1]
            splitted = tmp_txt.split(f"[{link_txt}]({href})", 1)
            if len(splitted[0]) != 0:
                nodes.append(TextNode(splitted[0], TextType.TEXT))
            nodes.append(TextNode(link_txt, TextType.LINK, href))
            if len(splitted[1]) == 0:
                continue
            if len(matches) > i + 1:
                tmp_txt = splitted[1]
            else:
                nodes.append(TextNode(splitted[1], TextType.TEXT))
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise Exception(f'Invalid syntax: "{delimiter}"')
        for i in range(len(splitted)):
            tmp_txt = splitted[i]
            if len(tmp_txt) == 0:
                continue
            if i % 2 == 0:
                nodes.append(TextNode(tmp_txt, TextType.TEXT))
            else:
                nodes.append(TextNode(tmp_txt, text_type))

    return nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes
