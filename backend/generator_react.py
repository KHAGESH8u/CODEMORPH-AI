SELF_CLOSING_TAGS = ["img", "br", "hr", "input", "meta", "link"]


def convert_attributes(attrs):
    result = ""
    for key, value in attrs.items():
        if key == "class":
            value = " ".join(value)
            key = "className"

        if key == "for":
            key = "htmlFor"

        if isinstance(value, str) and value.isdigit():
            result += f" {key}={{{value}}}"
        else:
            result += f' {key}="{value}"'

    return result


def generate_react(node, indent=0, in_pre=False):
    space = "" if in_pre else "  " * indent
    newline = "" if in_pre else "\n"

    # TEXT NODE
    if isinstance(node, str):
        if in_pre:
            # 🔥 THE FIX: Wrap the text in JSX template literals {` `}
            # This stops React from collapsing the spaces and newlines!
            escaped = node.replace("`", "\\`").replace("$", "\\$")
            return f"{{`{escaped}`}}"

        return space + node + "\n"

    tag = node.get("type", "div")

    if tag == "body":
        tag = "div"

    # 🔥 Reverted back to <pre> so it catches your index.html CSS
    if tag == "pre":
        attributes = convert_attributes(node.get("attributes", {}))
        opening = f"{space}<pre{attributes}>"
        children = node.get("children", [])

        result = opening + newline
        for child in children:
            # Pass in_pre=True to all children
            result += generate_react(child, indent + 1, in_pre=True)

        result += f"{space}</pre>{newline}"
        return result

    attributes = convert_attributes(node.get("attributes", {}))

    if tag in SELF_CLOSING_TAGS:
        return f"{space}<{tag}{attributes} />{newline}"

    opening = f"{space}<{tag}{attributes}>"
    children = node.get("children", [])

    result = opening + newline

    for child in children:
        result += generate_react(child, indent + 1, in_pre)

    result += f"{space}</{tag}>{newline}"

    if not in_pre:
        return result.rstrip() + "\n"

    return result
