from bs4 import BeautifulSoup, NavigableString


def parse_element(element):
    # Handle text nodes properly
    if isinstance(element, NavigableString):
        text = element.strip()
        return text if text else None

    node = {
        "type": element.name,
        "attributes": dict(element.attrs),
        "children": [],
    }

    for child in element.children:
        parsed_child = parse_element(child)
        if parsed_child:
            node["children"].append(parsed_child)

    return node


def html_to_ui_tree(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body if soup.body else soup
    return parse_element(body)
