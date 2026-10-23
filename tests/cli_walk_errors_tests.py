import os
from pathlib import Path

import pytest

from trafilatura.cli import parse_args, process_args


@pytest.mark.parametrize("kind", ["missing", "file"])
def test_invalid_input_directory_is_logged(tmp_path, caplog, kind):
    source = tmp_path / "input"
    if kind == "file":
        source.write_text("not a directory")
    args = parse_args(["--input-dir", str(source), "--parallel", "1"])
    with pytest.raises(SystemExit) as error:
        process_args(args)
    assert error.value.code == 1
    assert repr(str(source)) in caplog.text


@pytest.mark.skipif(
    os.name == "nt" or getattr(os, "geteuid", lambda: 0)() == 0,
    reason="Requires POSIX directory permissions and an unprivileged user",
)
def test_unreadable_directory_does_not_skip_readable_files(tmp_path, caplog):
    source = tmp_path / "inputs"
    source.mkdir()
    blocked = source / "blocked"
    blocked.mkdir()
    (blocked / "hidden.html").write_text("input")
    readable = source / "readable"
    readable.mkdir()
    fixture = Path(__file__).parent / "resources/httpbin_sample.html"
    (source / "top.html").write_bytes(fixture.read_bytes())
    (readable / "nested.html").write_bytes(fixture.read_bytes().replace(b"blacksmith", b"carpenter"))
    output = tmp_path / "output"
    args = parse_args(["--input-dir", str(source), "--output-dir", str(output), "--parallel", "1", "--fast"])
    blocked.chmod(0)
    try:
        with pytest.raises(SystemExit) as error:
            process_args(args)
        assert error.value.code == 1
        assert str(blocked) in caplog.text
        results = [path.read_text(encoding="utf-8") for path in output.rglob("*.txt")]
        assert len(results) == 2
        assert any("blacksmith" in result for result in results)
        assert any("carpenter" in result for result in results)
    finally:
        blocked.chmod(0o700)
