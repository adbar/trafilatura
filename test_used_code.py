

html_content = """
        <!DOCTYPE html>
        <html>wh
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
            <p>This is a test paragraph.</p>
            <div class="content">
                <p>Content inside a div.</p>
            </div>
        </body>
        </html>
        """


import requests
from trafilatura.main import extract_html_into_markdown

with open("quantum_neural_network_raw.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()
with open("quantum_neural_network.txt", "r", encoding="utf-8") as markdown_file:
    markdown_content = markdown_file.read()

text = extract_html_into_markdown(html_content)
assert markdown_content == text
#TODO: assert diff is null
