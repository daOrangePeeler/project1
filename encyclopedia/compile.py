def start_block(block_name):
    return "{%  block " + block_name + " %}"

def end_block(block_name=None):
    if block_name is not None:
        return "{% endblock " + block_name + " %}"
    else:
        return "{% endblock %}"

def create(entry_name, html_body):
    extends_string = "{% extends \"/encyclopledia/layout.html\" %}"
    body = html_body
    title = entry_name

    html = extends_string + start_block("title") + entry_name + end_block("title") + start_block("body") + html_body + end_block("body")

    return html