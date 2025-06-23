import pytest
from pathlib import Path

@pytest.fixture
def html_content():
    return (Path(__file__).parent / "test_markdown_extraction" / "quantum_neural_network_raw.html").read_text(encoding="utf-8")

@pytest.fixture
def expected_md():
    return (Path(__file__).parent / "test_markdown_extraction" / "quantum_neural_network.txt").read_text(encoding="utf-8")