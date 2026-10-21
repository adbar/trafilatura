import pickle
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import get_context
from pathlib import Path
from time import sleep

import pytest

from trafilatura import cli_utils, settings
from trafilatura.cli import parse_args
from trafilatura.cli_utils import file_processing_pipeline


def test_worker_returns_serializable_details_for_unpickleable_errors():
    class ProcessingError(Exception):
        pass

    error = ProcessingError("could not write output")
    with pytest.raises((AttributeError, TypeError, pickle.PicklingError)):
        pickle.dumps(error)

    def fail(_filename):
        raise error

    result = cli_utils._file_processing_worker(fail, "page.html")
    assert result == "ProcessingError could not write output"
    assert pickle.loads(pickle.dumps(result)) == result


def test_worker_passes_the_filename_and_reports_success():
    processed = []
    assert cli_utils._file_processing_worker(processed.append, "page.html") is None
    assert processed == ["page.html"]


@pytest.mark.parametrize("error", [KeyboardInterrupt(), SystemExit(2)])
def test_worker_does_not_swallow_control_flow(error):
    def fail(_filename):
        raise error

    with pytest.raises(type(error)):
        cli_utils._file_processing_worker(fail, "page.html")


@pytest.mark.parametrize("start_method", [None, "spawn"])
@pytest.mark.parametrize("batch_size", [2, 1000])
def test_file_errors_are_logged_without_skipping_valid_files(tmp_path, monkeypatch, caplog, start_method, batch_size):
    source = tmp_path / "inputs"
    source.mkdir()
    fixture = Path(__file__).parent / "resources/httpbin_sample.html"
    files = []
    for name in ["missing-first.html", "first.html", "missing-second.html", "second.html"]:
        filename = source / name
        if name.startswith("missing"):
            try:
                filename.symlink_to(tmp_path / name)
            except OSError as error:
                pytest.skip(f"Cannot create symlink on this system {error}")
        else:
            replacement = b"blacksmith" if name == "first.html" else b"carpenter"
            filename.write_bytes(fixture.read_bytes().replace(b"blacksmith", replacement))
        files.append(str(filename))
    monkeypatch.setattr(cli_utils, "generate_filelist", lambda _inputdir, **_kwargs: iter(files))
    monkeypatch.setattr(cli_utils, "MAX_FILES_PER_DIRECTORY", batch_size)
    if start_method:
        monkeypatch.setattr(
            cli_utils,
            "ProcessPoolExecutor",
            partial(ProcessPoolExecutor, mp_context=get_context(start_method)),
        )
    output = tmp_path / "output"
    args = parse_args(["--input-dir", str(source), "--output-dir", str(output), "--parallel", "1", "--fast"])
    assert file_processing_pipeline(args) == 1
    results = [path.read_text(encoding="utf-8") for path in output.rglob("*.txt")]
    assert len(results) == 2
    assert all(any(name in result for result in results) for name in ["blacksmith", "carpenter"])
    failures = [record.message for record in caplog.records if "Cannot process file" in record.message]
    assert len(failures) == 2
    assert all(any(filename in message for message in failures) for filename in [files[0], files[2]])


def test_cli_returns_failure_after_processing_readable_files(tmp_path):
    source = tmp_path / "inputs"
    source.mkdir()
    try:
        (source / "missing.html").symlink_to(tmp_path / "missing-target.html")
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    fixture = Path(__file__).parent / "resources/httpbin_sample.html"
    (source / "page.html").write_bytes(fixture.read_bytes())
    output = tmp_path / "output"
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-c",
            "from trafilatura.cli import main; main()",
            "--input-dir",
            str(source),
            "--output-dir",
            str(output),
            "--parallel",
            "1",
            "--fast",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "missing.html" in result.stderr
    assert "Traceback" not in result.stderr
    results = list(output.rglob("*.txt"))
    assert len(results) == 1
    assert results[0].read_text(encoding="utf-8").strip()


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
    assert file_processing_pipeline(args) == 0
    files = list(output.rglob("*.txt"))
    assert len(files) == 1
    assert files[0].read_text(encoding="utf-8").strip()


def test_empty_input_directory_still_succeeds(tmp_path):
    args = parse_args(["--input-dir", str(tmp_path), "--parallel", "1"])
    assert file_processing_pipeline(args) == 0


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
