from pathlib import Path

import pytest

from trafilatura import cli_utils
from trafilatura.cli import parse_args


def pipeline_inputs(args, monkeypatch):
    seen = []

    class RecordingExecutor:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def map(self, function, paths, **kwargs):
            seen.extend(paths)
            return iter(())

    monkeypatch.setattr(cli_utils, "ProcessPoolExecutor", RecordingExecutor)
    cli_utils.file_processing_pipeline(args)
    return {Path(name).relative_to(args.input_dir).as_posix() for name in seen}


def make_inputs(tmp_path):
    source = tmp_path / "input"
    source.mkdir()
    for name in ["original.html", "generated/old.txt", "backups/page.html", "other/page.html"]:
        target = source / name
        target.parent.mkdir(exist_ok=True)
        target.write_text("input")
    return source


@pytest.mark.parametrize("destination", ["output", "backup", "both"])
def test_pipeline_excludes_only_configured_destinations(tmp_path, monkeypatch, destination):
    source = make_inputs(tmp_path)
    options = ["--input-dir", str(source), "--parallel", "1"]
    expected = {"original.html", "generated/old.txt", "backups/page.html", "other/page.html"}
    if destination in {"output", "both"}:
        options.extend(["--output-dir", str(source / "generated")])
        expected.remove("generated/old.txt")
    if destination in {"backup", "both"}:
        options.extend(["--backup-dir", str(source / "backups")])
        expected.remove("backups/page.html")
    assert pipeline_inputs(parse_args(options), monkeypatch) == expected


def test_relative_destination_paths_are_normalized(tmp_path, monkeypatch):
    make_inputs(tmp_path)
    monkeypatch.chdir(tmp_path)
    args = parse_args(
        [
            "--input-dir",
            "input",
            "--parallel",
            "1",
            "--output-dir",
            "input/generated/../generated",
        ]
    )
    assert pipeline_inputs(args, monkeypatch) == {"original.html", "backups/page.html", "other/page.html"}


def test_external_destinations_do_not_exclude_inputs(tmp_path, monkeypatch):
    source = make_inputs(tmp_path)
    args = parse_args(
        [
            "--input-dir",
            str(source),
            "--parallel",
            "1",
            "--output-dir",
            str(tmp_path / "output"),
            "--backup-dir",
            str(tmp_path / "backup"),
        ]
    )
    assert len(pipeline_inputs(args, monkeypatch)) == 4


def test_unconfigured_directories_are_not_excluded(tmp_path, monkeypatch):
    source = make_inputs(tmp_path)
    args = parse_args(["--input-dir", str(source), "--parallel", "1"])
    assert len(pipeline_inputs(args, monkeypatch)) == 4


def test_directory_symlink_is_not_followed(tmp_path, monkeypatch):
    source = make_inputs(tmp_path)
    try:
        (source / "loop").symlink_to(source, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    args = parse_args(
        [
            "--input-dir",
            str(source),
            "--parallel",
            "1",
            "--output-dir",
            str(tmp_path / "outside"),
        ]
    )
    assert len(pipeline_inputs(args, monkeypatch)) == 4


def test_input_directory_alias_still_excludes_physical_output(tmp_path, monkeypatch):
    source = make_inputs(tmp_path)
    alias = tmp_path / "input-alias"
    try:
        alias.symlink_to(source, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    args = parse_args(
        [
            "--input-dir",
            str(alias),
            "--parallel",
            "1",
            "--output-dir",
            str(source / "generated"),
        ]
    )
    assert pipeline_inputs(args, monkeypatch) == {"original.html", "backups/page.html", "other/page.html"}


def test_output_directory_alias_excludes_physical_destination(tmp_path, monkeypatch):
    source = make_inputs(tmp_path)
    alias = tmp_path / "output-alias"
    try:
        alias.symlink_to(source / "generated", target_is_directory=True)
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    args = parse_args(
        [
            "--input-dir",
            str(source),
            "--parallel",
            "1",
            "--output-dir",
            str(alias),
        ]
    )
    assert pipeline_inputs(args, monkeypatch) == {"original.html", "backups/page.html", "other/page.html"}
