


from trafilatura.main import extract_html_into_markdown


def test_extract(html_content, expected_md):
    actual_md = extract_html_into_markdown(html_content)
    assert actual_md == expected_md
    


