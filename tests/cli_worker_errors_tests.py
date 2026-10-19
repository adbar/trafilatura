from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import get_context
from pathlib import Path
from time import sleep

import pytest

from trafilatura import cli_utils, settings
from trafilatura.cli import parse_args
from trafilatura.cli_utils import file_processing_pipeline


def test_file_read_error_reaches_the_caller(tmp_path):
    source = tmp_path / "inputs"
    source.mkdir()
    try:
        (source / "missing.html").symlink_to(tmp_path / "missing-target.html")
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    args = parse_args(["--input-dir", str(source), "--parallel", "1"])
    with pytest.raises(FileNotFoundError):
        file_processing_pipeline(args)


@pytest.mark.parametrize("extraction_timeout", [None, 0])
def test_local_file_processing_still_writes_output(tmp_path, extraction_timeout):
    source = tmp_path / "inputs"
    source.mkdir()
    fixture = Path(__file__).parent / "resources/httpbin_sample.html"
    (source / "page.html").write_bytes(fixture.read_bytes())
    output = tmp_path / "output"
    args = parse_args(
        [
            "--input-dir",
            str(source),
            "--output-dir",
            str(output),
            "--parallel",
            "1",
            "--fast",
        ]
    )
    if extraction_timeout is not None:
        config = settings.use_config()
        config.set("DEFAULT", "EXTRACTION_TIMEOUT", str(extraction_timeout))
        config_file = tmp_path / "settings.cfg"
        with config_file.open("w", encoding="utf-8") as config_output:
            config.write(config_output)
        args.config_file = str(config_file)
    file_processing_pipeline(args)
    files = list(output.rglob("*.txt"))
    assert len(files) == 1
    assert files[0].read_text(encoding="utf-8").strip()


def test_empty_input_directory_still_succeeds(tmp_path):
    args = parse_args(["--input-dir", str(tmp_path), "--parallel", "1"])
    assert file_processing_pipeline(args) is None


def mark_processed_file(filename, args, counter=-1, options=None):
    sleep(0.6)
    Path(filename).with_suffix(".done").touch()


@pytest.mark.parametrize("start_method", [None, "spawn"])
def test_extraction_timeout_is_not_a_batch_deadline(tmp_path, monkeypatch, start_method):
    source = tmp_path / "inputs"
    source.mkdir()
    for name in ["first.html", "second.html"]:
        (source / name).write_text("input")
    config = settings.use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", "1")
    config_file = tmp_path / "settings.cfg"
    with config_file.open("w", encoding="utf-8") as config_output:
        config.write(config_output)
    args = parse_args(
        [
            "--input-dir",
            str(source),
            "--parallel",
            "1",
            "--config-file",
            str(config_file),
        ]
    )
    monkeypatch.setattr(cli_utils, "file_processing", mark_processed_file)
    if start_method:
        monkeypatch.setattr(
            cli_utils,
            "ProcessPoolExecutor",
            partial(ProcessPoolExecutor, mp_context=get_context(start_method)),
        )
    file_processing_pipeline(args)
    assert {path.name for path in source.glob("*.done")} == {"first.done", "second.done"}
