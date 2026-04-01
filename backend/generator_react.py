SELF_CLOSING_TAGS = ["img", "br", "hr", "input", "meta", "link"]


def convert_style_string(style_str):
    """Converts 'color: red; margin-top: 10px;' to '{{ color: "red", marginTop: "10px" }}'"""
    if not style_str:
        return "{}"

    styles = []
    # Split by semicolon to get individual CSS rules
    for declaration in style_str.split(";"):
        if ":" not in declaration:
            continue

        prop, val = declaration.split(":", 1)
        prop = prop.strip()
        val = val.strip()

        # Convert kebab-case (margin-top) to camelCase (marginTop)
        parts = prop.split("-")
        camel_prop = parts[0] + "".join(word.capitalize() for word in parts[1:])

        styles.append(f'{camel_prop}: "{val}"')

    return "{{ " + ", ".join(styles) + " }}"


def convert_attributes(attrs):
    result = ""
    for key, value in attrs.items():
        if key == "class":
            # BeautifulSoup parses classes as a list
            value = " ".join(value) if isinstance(value, list) else value
            key = "className"

        elif key == "for":
            key = "htmlFor"

        elif key == "style":
            # 🔥 Send the CSS string to our new parser
            style_obj = convert_style_string(value)
            result += f" style={style_obj}"
            continue  # Skip the default string formatting below

        # Default attribute handling
        if isinstance(value, str) and value.isdigit():
            result += f" {key}={{{value}}}"
        elif isinstance(value, list):
            result += f' {key}="{" ".join(value)}"'
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

    # 🔥 FIX: Catch all of BeautifulSoup's invisible wrapper tags
    if tag in ["body", "[document]", "html"]:
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
