

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
from trafilatura import extract

# Define the URL
url = "https://en.wikipedia.org/wiki/Quantum_neural_network"

# Fetch the HTML content from the URL
response = requests.get(url)
html_content = response.text

# Extract readable text from HTML
text = extract(
    html_content,
    include_links=False,
    include_tables=False,
    include_formatting=True,
    output_format='markdown',
    fast=True,
)

print("text:", text)

if text:
    with open("quantum_neural_network.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Saved to quantum_neural_network.txt")
else:
    print("Extraction failed or returned no content.")
