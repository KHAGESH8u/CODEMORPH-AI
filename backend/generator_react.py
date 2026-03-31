SELF_CLOSING_TAGS = ["img", "br", "hr", "input", "meta", "link"]


def convert_attributes(attrs):
    result = ""

    for key, value in attrs.items():
        if key == "class":
            value = " ".join(value)
            key = "className"

        if key == "for":
            key = "htmlFor"

        # 🔥 Change 4: numeric values → JSX format
        if isinstance(value, str) and value.isdigit():
            result += f" {key}={{{value}}}"
        else:
            result += f' {key}="{value}"'

    return result


def generate_react(node, indent=0):
    space = "  " * indent

    # Text node
    if isinstance(node, str):
        return space + node.strip() + "\n"

    tag = node.get("type", "div")

    if tag == "body":
        tag = "div"

    attributes = convert_attributes(node.get("attributes", {}))

    # Self-closing tags
    if tag in SELF_CLOSING_TAGS:
        return f"{space}<{tag}{attributes} />\n"

    opening = f"{space}<{tag}{attributes}>"
    children = node.get("children", [])

    result = opening + "\n"

    for child in children:
        result += generate_react(child, indent + 1)

    result += f"{space}</{tag}>\n"

    # 🔥 Change 3: remove trailing spaces
    return result.rstrip() + "\n"
