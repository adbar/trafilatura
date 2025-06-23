from trafilatura import _internal_extraction

def extract_html_into_markdown(html_content: str) -> str:
    document = _internal_extraction(
        filecontent=html_content,
        include_links=False,
        include_images=False,
        output_format='markdown',
    )
    markdown_text = document.text
    return markdown_text