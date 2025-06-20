

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
from trafilatura import _internal_extraction

# # Define the URL
# url = "https://en.wikipedia.org/wiki/Quantum_neural_network"

# # Fetch the HTML content from the URL
# response = requests.get(url)
# html_content = response.text
# with open("quantum_neural_network_raw.html", "w", encoding="utf-8") as html_file:
#     html_file.write(html_content)

# Extract readable text from HTML

# Load the HTML content from file
with open("quantum_neural_network_raw.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()
    
document = _internal_extraction(
    filecontent=html_content,
    include_links=False,
    include_tables=False,
    include_formatting=False,
    include_images=False,
    output_format='markdown',
    # favor_precision=True,
    # include_comments=False,
    # tei_validation=True,
)
text = document.text
# filecontent: Any,
# url: str | None = None,
# record_id: str | None = None,
# fast: bool = False,
# no_fallback: bool = False,
# favor_precision: bool = False,
# favor_recall: bool = False,
# include_comments: bool = True,
# output_format: str = "txt",
# tei_validation: bool = False,
# target_language: str | None = None,
# include_tables: bool = True,
# include_images: bool = False,
# include_formatting: bool = False,
# include_links: bool = False,
# deduplicate: bool = False,
# date_extraction_params: Dict[str, Any] | None = None,
# with_metadata: bool = False,
# only_with_metadata: bool = False,
# max_tree_size: int | None = None,
# url_blacklist: Set[str] | None = None,
# author_blacklist: Set[str] | None = None,
# settingsfile: str | None = None,
# prune_xpath: Any | None = None,
# config: Any = DEFAULT_CONFIG,
# options: Extractor | None = None

print("text:", text)

if text:
    with open("quantum_neural_network.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Saved to quantum_neural_network.txt")
else:
    print("Extraction failed or returned no content.")
