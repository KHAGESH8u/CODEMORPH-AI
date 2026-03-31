from bs4 import BeautifulSoup, NavigableString


def parse_element(element, in_pre=False):
    # Handle text nodes
    if isinstance(element, NavigableString):
        text = str(element)

        if in_pre:
            return text  # keep spaces

        text = text.strip()
        return text if text else None

    tag = element.name

    node = {
        "type": tag,
        "attributes": dict(element.attrs),
        "children": [],
    }

    # Detect <pre>
    if tag == "pre":
        in_pre = True

    for child in element.children:
        parsed_child = parse_element(child, in_pre)
        if parsed_child:
            node["children"].append(parsed_child)

    return node


def html_to_ui_tree(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body if soup.body else soup
    return parse_element(body)
