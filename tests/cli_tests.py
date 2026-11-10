"""
Unit tests for the command-line interface.
"""

import csv
import gzip
import io
import logging
import os
import random
import re
import shutil
import subprocess
import sys
import sysconfig
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from multiprocessing import get_all_start_methods
from os import path
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from courlan import UrlStore

from trafilatura import cli, cli_utils, settings, spider
from trafilatura.downloads import Response, add_to_compressed_dict, fetch_response
from trafilatura.utils import LANGID_FLAG

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
RESOURCES_DIR = path.join(path.abspath(path.dirname(__file__)), "resources")
# the entry point next to the running interpreter, even if its directory is not on PATH
TRAFILATURA_BIN = shutil.which("trafilatura", path=sysconfig.get_path("scripts")) or "trafilatura"


def test_random_filenames_leave_callers_random_state_unchanged(tmp_path):
    """Generating a filename must not advance the caller's random state."""
    state = random.getstate()
    cli_utils.get_writable_path(str(tmp_path), ".txt")
    assert random.getstate() == state


pytestmark = pytest.mark.usefixtures("mock_network")


@pytest.fixture
def run(capsys):
    "In-process CLI run: exit code, STDOUT, STDERR."

    def _run(argv):
        capsys.readouterr()
        try:
            cli.process_args(cli.parse_args(argv))
            code = 0
        except SystemExit as exit_info:
            code = exit_info.code
        captured = capsys.readouterr()
        return code, captured.out, captured.err

    return _run


def test_version(run):
    code, out, _ = run(["--version"])
    assert code == 0
    assert re.match(r"Trafilatura [0-9]\.[0-9]+\.[0-9] - Python [0-9]\.[0-9]+\.[0-9]", out)


@pytest.mark.parametrize("fmt", ["csv", "html", "json", "markdown", "xml", "xmltei"])
def test_format_flags(fmt):
    assert cli.parse_args([f"--{fmt}"]).output_format == fmt


def test_url_filter_values():
    assert cli.parse_args(["--url-filter", "test1", "test2"]).url_filter == ["test1", "test2"]


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no named pipes")
@pytest.mark.parametrize("extra", [["-i"], ["-u", "https://example.org", "-b"]])
def test_input_from_pipe(tmp_path, extra):
    "Pipes and /dev/stdin pass the file checks."
    os.mkfifo(tmp_path / "fifo")
    assert cli.parse_args([*extra, str(tmp_path / "fifo")])


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no named pipes")
def test_config_file_from_pipe(tmp_path, run):
    "The config file is read several times, a pipe is rejected."
    os.mkfifo(tmp_path / "fifo")
    code, _, err = run(["-u", "https://example.org", "--config-file", str(tmp_path / "fifo")])
    assert code == 2
    assert "--config-file: not a file" in err


@pytest.mark.skipif(os.name == "nt" or os.geteuid() == 0, reason="needs POSIX permissions as non-root")
def test_input_file_unreadable_parent(tmp_path, run):
    "A file in an unreadable directory is reported, not a traceback."
    locked = tmp_path / "locked"
    locked.mkdir()
    (locked / "list.txt").write_text("https://example.org\n")
    locked.chmod(0)
    try:
        code, _, err = run(["-i", str(locked / "list.txt")])
    finally:
        locked.chmod(0o700)
    assert code == 2
    assert "-i/--input-file: Permission denied" in err


@pytest.mark.parametrize(
    "content, message",
    [
        ("MIN_OUTPUT_SIZE = 1\n", "File contains no section headers"),
        ("[DEFAULT]\nMIN_EXTRACTED_SIZE = 250.5\n", "invalid literal for int()"),
        ("[DEFAULT]\nEXTENSIVE_DATE_SEARCH = maybe\n", "Not a boolean: maybe"),
        # download settings are read lazily, their types must be checked up front too
        ("[DEFAULT]\nSLEEP_TIME = abc\n", "could not convert string to float: 'abc'"),
        ("[DEFAULT]\nMAX_REDIRECTS = x\n", "invalid literal for int()"),
        ("[DEFAULT]\nSSRF_PROTECTION = maybe\n", "Not a boolean: maybe"),
    ],
)
def test_config_file_malformed_content(tmp_path, run, content, message):
    "A config file with bad syntax or types is an argument error, not a traceback."
    cfg = tmp_path / "bad.cfg"
    cfg.write_text(content, encoding="utf-8")
    code, _, err = run(["-u", "https://example.org", "--config-file", str(cfg)])
    assert code == 2
    assert "--config-file: " in err
    assert message in err


def test_config_file_non_utf8(tmp_path, run):
    "A non-UTF-8 config file is an argument error, not a UnicodeDecodeError traceback."
    cfg = tmp_path / "bad.cfg"
    cfg.write_bytes(b"[DEFAULT]\nMIN_OUTPUT_SIZE = 1\n\xff\xfe")
    code, _, err = run(["-u", "https://example.org", "--config-file", str(cfg)])
    assert code == 2
    assert "--config-file: " in err


@pytest.mark.skipif(os.name == "nt" or os.geteuid() == 0, reason="needs POSIX permissions as non-root")
@pytest.mark.parametrize(
    "option, label", [("-i", "-i/--input-file"), ("-b", "-b/--blacklist"), ("--config-file", "--config-file")]
)
def test_unreadable_file(tmp_path, run, option, label):
    "A file that exists but cannot be read is reported, not a traceback."
    unreadable = tmp_path / "list.txt"
    unreadable.write_text("https://example.org\n")
    unreadable.chmod(0)
    argv = [option, str(unreadable)] if option == "-i" else ["-u", "https://example.org", option, str(unreadable)]
    try:
        code, _, err = run(argv)
    finally:
        unreadable.chmod(0o600)
    assert code == 2
    assert f"{label}: cannot read" in err


@pytest.mark.parametrize(
    "flags, level", [([], logging.WARNING), (["-v"], logging.INFO), (["-vv"], logging.DEBUG), (["-vvv"], logging.DEBUG)]
)
def test_verbosity_levels(tmp_path, run, flags, level):
    with patch.object(cli.logging, "basicConfig") as config:
        run(["--input-dir", str(tmp_path), *flags])
    assert config.call_args.kwargs["level"] == level


@pytest.mark.parametrize("filters", [["-b", "blacklist"], ["--url-filter", "/news/"]])
@pytest.mark.parametrize("option, fetcher", [("--crawl", "buffered_response_downloads"), ("--probe", "buffered_downloads")])
def test_seed_filters(tmp_path, filters, option, fetcher, run):
    "Crawler and probe start URLs go through the blacklist and URL filter."
    (tmp_path / "blacklist").write_text("https://example.org/start\n", encoding="utf-8")
    filters = [str(tmp_path / f) if f == "blacklist" else f for f in filters]
    with patch.object(cli_utils, fetcher, return_value=[]) as fetch:
        code, out, _ = run([option, "https://example.org/start", *filters])
    # no start URL left is an input error
    assert code == 1
    assert all(not c.args[0] for c in fetch.call_args_list)
    assert not out.strip()


def test_probe_skips_failed_and_short_pages(run):
    pages = [("https://example.org/", None), ("https://example.org/short", "<html><body><p>Short text.</p></body></html>")]
    with patch.object(cli_utils, "buffered_downloads", return_value=pages):
        assert not run(["--probe", "https://example.org/"])[1].strip()


@pytest.mark.parametrize(
    "errors, archived_errors, expected",
    [
        ([], [], 0),
        (["https://example.org/a"], [], 0),
        # the ratio is computed over all input URLs
        (["https://example.org/a"], ["archived"], 1),
        (["https://example.org/a", "https://example.org/b"], ["archived1", "archived2"], 126),
    ],
)
def test_archived_retry_exit_code(errors, archived_errors, expected):
    args = cli.parse_args(["-u", "https://example.org/a", "--archived"])
    url_store = add_to_compressed_dict(["https://example.org/a", "https://example.org/b"])
    results = iter([(errors, -1), (archived_errors, -1)])
    with patch.object(cli_utils, "download_queue_processing", side_effect=lambda *a: next(results)) as download:
        assert cli_utils.url_processing_pipeline(args, url_store) == expected
    assert download.call_count == (2 if errors else 1)
    if errors:
        archived = download.call_args.args[0].dump_urls()
        assert all(u.startswith("https://web.archive.org/web/20/") for u in archived)
        assert len(archived) == len(errors)


@pytest.mark.parametrize(
    "url, prefix",
    [
        ("https://www.example.com/page3", "www.example.com_page3-"),
        ("https://user:password@example.com/a%20b?q=secret", "example.com_a_b-"),
        ("https://example.com/../../CON:a?b=1", "example.com_.._.._CON_a-"),
        ("https://example.com/" + "x" * 500, "example.com_"),
        ("https://example.com/中文", "example.com-"),
        ("https://例子.测试/中文", "-"),
    ],
    ids=["readable", "credentials-and-query", "unsafe-characters", "long-path", "unicode", "empty-prefix"],
)
def test_url_filenames_are_portable(url, prefix):
    filename = cli_utils.generate_url_filename(url)
    assert filename.startswith(prefix)
    assert re.fullmatch(r"[A-Za-z0-9._-]*-[a-f0-9]{16}", filename)
    assert len(filename) <= 137
    assert filename == cli_utils.generate_url_filename(url)


def test_url_filename_blake2b_suffix():
    assert cli_utils.generate_url_filename("https://www.example.com/page3") == "www.example.com_page3-67eb6bd757a48a52"


@pytest.mark.parametrize(
    "urls",
    [
        ("https://example.com/a/b", "https://example.com/a_b"),
        ("https://example.com/page?a=1", "https://example.com/page?a=2"),
        ("http://example.com/page", "https://example.com/page"),
        ("https://example.com/Page", "https://example.com/page"),
        ("https://example.com/" + "x" * 500 + "a", "https://example.com/" + "x" * 500 + "b"),
    ],
    ids=["sanitized-path", "query", "scheme", "case-insensitive-filesystem", "truncated-path"],
)
def test_url_filenames_distinguish_urls(urls):
    assert cli_utils.generate_url_filename(urls[0]).lower() != cli_utils.generate_url_filename(urls[1]).lower()


def test_url_mode_passes_url(caplog, capsys):
    "In URL mode, the extraction and the size check get the downloaded URL."
    args = cli.parse_args(["-u", "https://example.org/page", "--xml", "--with-metadata"])
    html = Path(RESOURCES_DIR, "httpbin_sample.html").read_text(encoding="utf-8")
    pages = [("https://example.org/page", html), ("https://example.org/short", "<p>x</p>")]
    with patch.object(cli_utils, "buffered_downloads", return_value=pages):
        assert cli_utils.url_processing_pipeline(args, cli_utils.load_input_dict(args)) == 0
    assert 'url="https://example.org/page"' in capsys.readouterr().out
    assert "too small/incorrect for URL https://example.org/short" in caplog.text


@pytest.mark.parametrize("backup", [False, True], ids=["extraction", "paired-backup"])
@pytest.mark.parametrize("counter", [-1, 0], ids=["flat-directory", "counter-directory"])
def test_url_filenames_write_results(tmp_path, backup, counter):
    output_dir, backup_dir = tmp_path / "output", tmp_path / "backup"
    args = cli.parse_args(["--name-from-url", "-o", str(output_dir), "-u", "https://example.org/", "--json"])
    if backup:
        args.backup_dir = str(backup_dir)
    options = settings.args_to_extractor(args)
    html = Path(RESOURCES_DIR, "httpbin_sample.html").read_text(encoding="utf-8")
    urls = ["https://example.org/a/b", "https://example.org/a_b"]
    for url in urls:
        assert cli_utils.process_result(html, args, counter, options, url) == (counter + 1 if counter >= 0 else -1)
    files = sorted(output_dir.rglob("*.json"))
    assert len(files) == 2
    assert all(file.name.startswith("example.org_a_b-") for file in files)
    assert all("Availing himself" in file.read_text(encoding="utf-8") for file in files)
    assert all(file.parent == (output_dir if counter < 0 else output_dir / "1") for file in files)
    if backup:
        for file in files:
            archive = backup_dir / file.relative_to(output_dir).with_suffix(".html.gz")
            with gzip.open(archive, "rt", encoding="utf-8") as saved:
                assert saved.read() == html


def test_hash_output_filename():
    args = cli.parse_args(["--input-dir", "myinputdir", "-o", "test"])
    assert cli_utils.determine_output_path(args, "testfile.txt", "")[0] == path.join("test", "uOHdo6wKo4IK0pkL.txt")


def test_archive_html(tmp_path):
    name = cli_utils.archive_html("<p>x</p>", cli.parse_args(["--backup-dir", str(tmp_path)]))
    with gzip.open(tmp_path / f"{name}.html.gz", "rt", encoding="utf-8") as saved:
        assert saved.read() == "<p>x</p>"


def test_writable_path_skips_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(cli_utils, "_FILENAME_RANDOM", random.Random(1))
    first, _ = cli_utils.get_writable_path(str(tmp_path), ".txt")
    Path(first).touch()
    monkeypatch.setattr(cli_utils, "_FILENAME_RANDOM", random.Random(1))
    assert cli_utils.get_writable_path(str(tmp_path), ".txt")[0] != first


def test_unwritable_destination_writes_nothing(tmp_path):
    (tmp_path / "blocker").write_text("")
    target = str(tmp_path / "blocker" / "out")
    cli_utils.write_result("text", cli.parse_args(["-o", target]))
    cli_utils.archive_html("<p>x</p>", cli.parse_args(["--backup-dir", target]))
    assert list(tmp_path.iterdir()) == [tmp_path / "blocker"]


@pytest.mark.parametrize("batch", [False, True], ids=["single-url", "url-list"])
def test_url_filenames_cli_download(tmp_path, batch, run):
    args_list = ["--name-from-url", "-o", str(tmp_path / "output")]
    if batch:
        input_file = tmp_path / "urls.txt"
        input_file.write_text("https://example.org/\nhttps://httpbun.com/html\n", encoding="utf-8")
        args_list.extend(["-i", str(input_file)])
    else:
        args_list.extend(["-u", "https://example.org/"])
    assert run(args_list)[0] == 0
    files = list((tmp_path / "output").rglob("*.txt"))
    assert len(files) == (2 if batch else 1)
    assert any(file.name.startswith("example.org-") for file in files)
    if batch:
        assert any(file.name.startswith("httpbun.com_html-") for file in files)
    assert all("Availing himself" in file.read_text(encoding="utf-8") for file in files)


def test_url_filenames_ignored_for_list(run):
    code, out, err = run(["--name-from-url", "--list", "-u", "https://example.org/", "-o", "output"])
    assert code == 0
    assert "--name-from-url" in err
    assert out.strip() == "https://example.org/"


def test_list_ignores_extraction_opts(capsys):
    "--list warns about extraction/format options that have no effect in list mode."
    cli.parse_args(["--list", "--json", "--no-comments", "--with-metadata"])
    err = capsys.readouterr().err
    assert "these options are ignored: --no-comments, --output-format, --with-metadata" in err


def test_list_ignores_output_and_tei_opts(capsys):
    "--list also ignores the output directory and TEI validation."
    cli.parse_args(["--list", "-u", "https://example.org/", "-o", "out", "--validate-tei"])
    err = capsys.readouterr().err
    assert "these options are ignored: --output-dir, --validate-tei" in err


def test_list_ignores_target_language(capsys):
    "--list ignores the target language unless the navigation options filter by it."
    cli.parse_args(["--list", "-u", "https://example.org/", "--target-language", "de"])
    err = capsys.readouterr().err
    assert "--target-language" in err
    assert "ignored" in err

    for nav in ("--feed", "--sitemap", "--crawl", "--explore", "--probe"):
        capsys.readouterr()
        cli.parse_args(["--list", nav, "https://example.org/x", "--target-language", "de"])
        assert "ignored" not in capsys.readouterr().err


def test_help(run):
    code, out, _ = run(["--help"])
    assert code == 0
    assert out.startswith("usage:")
    assert "--input-dir" in out


def test_args_to_extractor_kwargs():
    "args_to_extractor must propagate fast, images, links, comments, tables to Extractor."
    args = cli.parse_args(["--fast", "--images", "--links", "--no-comments", "--no-tables"])
    options = settings.args_to_extractor(args)
    assert options.fast is True
    assert options.images is True
    assert options.links is True
    assert options.comments is False
    assert options.tables is False


PAGE = (
    "<html><body><article>"
    + "".join(f"<p>Paragraph {i} " + "word " * 40 + "</p>" for i in range(5))
    + "</article></body></html>"
)


class _PageHandler(BaseHTTPRequestHandler):
    def _reply(self, body):
        self.send_response(200 if self.path.startswith(("/ok", "/tiny")) else 404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        if body and self.path.startswith("/ok"):
            self.wfile.write(PAGE.encode())
        elif body and self.path.startswith("/tiny"):
            # below MIN_FILE_SIZE
            self.wfile.write(b"<p>x</p>")

    def do_GET(self):
        self._reply(True)

    def do_HEAD(self):
        self._reply(False)

    def log_message(self, *_args):
        pass


@pytest.fixture(scope="module")
def cli_server(tmp_path_factory):
    server = ThreadingHTTPServer(("127.0.0.1", 0), _PageHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    tmp = tmp_path_factory.mktemp("exit")
    (tmp / "cfg").write_text("[DEFAULT]\nSSRF_PROTECTION = off\nSLEEP_TIME = 0\nDOWNLOAD_TIMEOUT = 5\n")
    for name, paths in (("partial", ["ok1", "dead1"]), ("dead", ["dead1", "dead2"]), ("empty", [])):
        (tmp / name).write_text("".join(f"{base}/{p}\n" for p in paths))
    # nothing listens on port 1: a second, unreachable host
    (tmp / "twohosts").write_text(f"{base}/ok\nhttp://127.0.0.1:1/\n")
    (tmp / "header").write_text(f"# my sites\n{base}/ok\n")
    (tmp / "in").mkdir()
    (tmp / "in" / "a.html").write_text(PAGE)
    (tmp / "blocker").write_text("")
    yield base, tmp
    server.shutdown()


def _run_cli(cli_server, argv, stdin=None, env=None):
    "Installed entry point, local server config unless reading STDIN."
    base, tmp = cli_server
    args = [arg.format(base=base, tmp=tmp) for arg in argv]
    if stdin is None:
        args += ["--config-file", str(tmp / "cfg")]
    return subprocess.run([TRAFILATURA_BIN, *args], input=stdin, capture_output=True, timeout=60, env=env)


@pytest.mark.parametrize(
    "argv, stdin, expected",
    [
        pytest.param(["--help"], None, 0, id="help"),
        pytest.param(["-u", "{base}/ok"], None, 0, id="url"),
        pytest.param(["-u", "{base}/dead"], None, 126, id="url-404"),
        pytest.param(["-u", "{base}/tiny"], None, 126, id="url-too-small"),
        pytest.param(["-i", "{tmp}/partial"], None, 1, id="list-partial"),
        pytest.param(["-i", "{tmp}/dead"], None, 126, id="list-dead"),
        pytest.param(["-i", "{tmp}/empty"], None, 1, id="list-empty"),
        pytest.param(["-u", "notaurl"], None, 1, id="url-invalid"),
        pytest.param(["-i", "{tmp}/partial", "--url-filter", "nomatch"], None, 1, id="list-filtered"),
        pytest.param(["-i", "{tmp}/missing"], None, 2, id="list-missing"),
        pytest.param(["--input-dir", "{tmp}/in"], None, 0, id="input-dir"),
        pytest.param(["--input-dir", "{tmp}/missing"], None, 1, id="input-dir-missing"),
        pytest.param(["--input-dir", "{tmp}/in", "-o", "{tmp}/blocker/out"], None, 1, id="output-unwritable"),
        pytest.param(["--input-dir", "{tmp}/in", "--backup-dir", "{tmp}/blocker/out"], None, 1, id="backup-unwritable"),
        pytest.param(["--input-dir", "{tmp}/in", "--list", "-o", "{tmp}/blocker/out"], None, 1, id="output-unwritable-list"),
        pytest.param([], PAGE.encode(), 0, id="stdin"),
        pytest.param([], b"<p>x</p>", 0, id="stdin-rejected"),
        pytest.param(["--crawl", "{base}/ok"], None, 0, id="crawl"),
        pytest.param(["--crawl", "{base}/dead"], None, 126, id="crawl-dead"),
        pytest.param(["--crawl", "notaurl"], None, 1, id="crawl-invalid"),
        pytest.param(["--probe", "{base}/ok"], None, 0, id="probe"),
        pytest.param(["--probe", "{base}/dead"], None, 126, id="probe-dead"),
        pytest.param(["--crawl", "-i", "{tmp}/twohosts"], None, 1, id="crawl-partial"),
        pytest.param(["--probe", "-i", "{tmp}/twohosts"], None, 1, id="probe-partial"),
        pytest.param(["--probe", "-i", "{tmp}/header"], None, 0, id="probe-header"),
        pytest.param(["--feed", "{base}/dead"], None, 1, id="feed-dead"),
        pytest.param(["--explore", "{base}/dead"], None, 126, id="explore-dead"),
    ],
)
def test_cli_exit_codes(cli_server, argv, stdin, expected):
    "The real CLI exit codes: 0 success, 1 some errors, 126 almost all inputs failed, 2 invalid arguments."
    result = _run_cli(cli_server, argv, stdin)
    assert result.returncode == expected, result.stderr.decode()[-300:]


@pytest.mark.parametrize("encoding", ["ascii", "utf-8"])
def test_cli_non_ascii_output(cli_server, encoding):
    "The entry point writes UTF-8 whatever the console encoding."
    page = "<html><body><article>" + ("<p>Größe, café, 中文 " + "mot " * 30 + "</p>") * 3 + "</article></body></html>"
    result = _run_cli(cli_server, [], page.encode("utf-8"), env={**os.environ, "PYTHONIOENCODING": encoding})
    assert result.returncode == 0
    assert "Größe, café, 中文" in result.stdout.decode("utf-8")


def test_cli_probe_prints_urls(cli_server):
    "--probe prints only the URLs with extractable content."
    result = _run_cli(cli_server, ["--probe", "-i", "{tmp}/partial"])
    assert result.stdout.decode().split() == [f"{cli_server[0]}/ok1"]


def test_input_type(capsys):
    testfile = "docs/trafilatura-demo.gif"
    with patch.object(sys, "argv", ["", "-u", "http"]), pytest.raises(SystemExit) as err:
        cli.main()
    assert err.value.code == 1
    args = cli.parse_args(["-v"])
    with open(testfile, "rb") as f:
        teststring = f.read(1024)
    assert cli.examine(teststring, args) is None
    assert cli.examine([1, 2, 3], args) is None
    testfile = "docs/usage.rst"
    with open(testfile, encoding="utf-8") as f:
        teststring = f.read()
    assert cli.examine(teststring, args) is None
    capsys.readouterr()
    assert cli.examine(None, args) is None
    assert "ERROR: empty document" in capsys.readouterr().err
    # test file list
    assert 10 <= len(list(cli_utils.generate_filelist(RESOURCES_DIR))) <= 21


@pytest.mark.parametrize(
    "stdin, tail",
    [
        pytest.param(
            b"<html><body><article>" + b"<p>Piped paragraph content.</p>" * 5 + b"</article></body></html>",
            "Piped paragraph content.",
            id="html",
        ),
        pytest.param(Path(RESOURCES_DIR, "webpage.html.gz").read_bytes(), "in deep-red West Virginia.", id="gzip"),
    ],
)
def test_cli_stdin(run, stdin, tail):
    "Plain and gzipped input on STDIN."
    with patch("sys.stdin") as mock_stdin:
        mock_stdin.buffer.read.return_value = stdin
        out = run(["-v"])[1]
    assert out.strip().endswith(tail)


def test_cli_examine_error(monkeypatch, capsys):
    "examine() swallows extraction errors and reports them on stderr."
    args = cli.parse_args(["-v"])

    def _boom(*args, **kwargs):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(cli_utils, "extract", _boom)
    html = "<html><body><article><p>" + "content " * 20 + "</p></article></body></html>"
    assert cli.examine(html, args) is None
    assert "kaboom" in capsys.readouterr().err


def test_sitemap_list(run):
    code, out, _ = run(["--sitemap", "https://sitemaps.org/sitemap.xml", "--list", "--parallel", "1"])
    assert code == 0
    assert out.strip().endswith("https://www.sitemaps.org/zh_TW/terms.html")


@pytest.mark.parametrize("output_args", [["--csv"], ["--output-format", "csv"]])
def test_csv_stdout_has_no_blank_records(tmp_path, output_args):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    for number in (1, 2):
        (input_dir / f"{number}.html").write_text(
            f"<html><body><article><p>Document {number} with some long enough text, here and there.</p>"
            "</article></body></html>",
            encoding="utf-8",
        )
    result = subprocess.run(
        [sys.executable, "-m", "trafilatura.cli", *output_args, "--input-dir", str(input_dir)],
        capture_output=True,
        check=True,
    )
    rows = list(csv.reader(io.StringIO(result.stdout.decode("utf-8"), newline=""), delimiter="\t"))
    assert [len(row) for row in rows] == [11, 11]
    assert {row[7] for row in rows} == {
        "Document 1 with some long enough text, here and there.",
        "Document 2 with some long enough text, here and there.",
    }
    expected = io.StringIO(newline="")
    csv.writer(expected, delimiter="\t").writerows(rows)
    assert result.stdout == expected.getvalue().encode("utf-8")


@pytest.mark.parametrize("newline", [None, "", "\r\n"])
@pytest.mark.parametrize(
    ("encoding", "stream_kind"),
    [
        ("utf-8", "file"),
        ("utf-8", "pipe"),
        ("cp1252", "file"),
        ("cp1252", "pipe"),
        ("utf-8-sig", "file"),
        ("utf-16", "file"),
    ],
)
@pytest.mark.parametrize("prefix", ["", "lead:"])
def test_csv_stdout_preserves_serialized_bytes(tmp_path, newline, encoding, stream_kind, prefix):
    args = cli.parse_args(["--csv"])
    rows = [["first\nsecond", "valué"], ["third", 'quoted "value"']]

    def capture(name, *, direct):
        output_path = tmp_path / name
        if stream_kind == "pipe":
            reader, writer = os.pipe()
            binary = os.fdopen(writer, "wb")
        else:
            binary = output_path.open("wb")
        # CRLF translation reproduces Windows behavior on every platform.
        with io.TextIOWrapper(binary, encoding=encoding, newline="" if direct else newline) as stdout:
            if prefix:
                stdout.write(prefix)
            with redirect_stdout(stdout):
                if direct:
                    csv.writer(stdout, delimiter="\t").writerows(rows)
                else:
                    for row in rows:
                        record = io.StringIO(newline="")
                        csv.writer(record, delimiter="\t").writerow(row)
                        cli_utils.write_result(record.getvalue(), args)
        if stream_kind == "pipe":
            with os.fdopen(reader, "rb") as pipe:
                return pipe.read()
        return output_path.read_bytes()

    assert capture("actual", direct=False) == capture("expected", direct=True)


def test_csv_stdout_text_capture(capsys):
    args = cli.parse_args(["--csv"])
    serialized = io.StringIO(newline="")
    rows = [["first\nsecond", "valué"], ["third", 'quoted "value"']]
    for row in rows:
        record = io.StringIO(newline="")
        csv.writer(record, delimiter="\t").writerow(row)
        cli_utils.write_result(record.getvalue(), args)
    csv.writer(serialized, delimiter="\t").writerows(rows)
    assert capsys.readouterr().out == serialized.getvalue()
    with redirect_stdout(io.StringIO(newline="")) as stdout:
        cli_utils.write_result(serialized.getvalue(), args)
    assert stdout.getvalue() == serialized.getvalue()


def test_csv_stdout_preserves_encoding_errors():
    args = cli.parse_args(["--csv"])
    with io.TextIOWrapper(io.BytesIO(), encoding="ascii", errors="replace", newline="\r\n") as stdout:
        with redirect_stdout(stdout):
            cli_utils.write_result("valué\r\n", args)
        stdout.flush()
        assert stdout.buffer.getvalue() == b"valu?\r\n"


@pytest.mark.parametrize("output_format", ["txt", "json", "xml"])
def test_non_csv_stdout_keeps_record_separator(capsys, output_format):
    args = cli.parse_args(["--output-format", output_format])
    cli_utils.write_result("first", args)
    cli_utils.write_result("second", args)
    assert capsys.readouterr().out == "first\nsecond\n"


@pytest.mark.parametrize("output_format", ["txt", "json", "xml"])
def test_non_csv_stdout_keeps_windows_translation(output_format):
    args = cli.parse_args(["--output-format", output_format])
    with io.TextIOWrapper(io.BytesIO(), encoding="utf-8-sig", newline="\r\n") as stdout:
        with patch.object(stdout, "reconfigure", wraps=stdout.reconfigure) as configure, redirect_stdout(stdout):
            cli_utils.write_result("first\nline", args)
            cli_utils.write_result("second", args)
        stdout.flush()
        assert stdout.buffer.getvalue() == "first\r\nline\r\nsecond\r\n".encode("utf-8-sig")
        configure.assert_not_called()


def test_csv_file_keeps_serialized_newline(tmp_path):
    args = cli.parse_args(["--csv", "-o", str(tmp_path)])
    serialized = io.StringIO(newline="")
    rows = [["first\nsecond", "valué"]]
    csv.writer(serialized, delimiter="\t").writerows(rows)
    record = serialized.getvalue()
    with io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="\r\n") as stdout:
        with patch.object(stdout, "reconfigure", wraps=stdout.reconfigure) as configure, redirect_stdout(stdout):
            cli_utils.write_result(record, args, new_filename="record")
        configure.assert_not_called()
    assert (tmp_path / "record.csv").read_bytes() == record.encode("utf-8")


def test_examine_options():
    html = Path(RESOURCES_DIR, "http_sample.html").read_text(encoding="utf-8")
    result = cli.examine(html, cli.parse_args(["--links", "--images"]))
    assert "[link](testlink.html)" in result
    assert "test.jpg" in result
    result = cli.examine(html, cli.parse_args(["--html"]))
    assert result.startswith("<html")
    assert result.endswith("</html>")


def test_input_files_with_bom(tmp_path):
    urls = tmp_path / "urls.txt"
    urls.write_bytes(b"\xef\xbb\xbfhttps://example.org/a\nhttps://example.org/b\n")
    args = cli.parse_args(["-i", str(urls)])
    assert cli_utils.load_input_urls(args) == ["https://example.org/a", "https://example.org/b"]
    blacklist = tmp_path / "blacklist.txt"
    blacklist.write_bytes(b"\xef\xbb\xbfhttps://example.org/a\n")
    assert cli_utils.load_blacklist(str(blacklist)) == {"https://example.org/a"}


def test_input_file_not_utf8(tmp_path, run):
    (tmp_path / "urls").write_bytes(b"https://example.org/\xe9\n")
    assert run(["-i", str(tmp_path / "urls")])[0] == "ERROR: system, file type or buffer encoding"


def test_file_processing_continues_after_error(tmp_path, caplog, run):
    source = tmp_path / "inputs"
    source.mkdir()
    missing = source / "missing.html"
    try:
        missing.symlink_to(tmp_path / "missing-target.html")
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    valid = source / "page.html"
    valid.write_bytes(Path(RESOURCES_DIR, "httpbin_sample.html").read_bytes())
    output = tmp_path / "output"
    argv = ["--input-dir", str(source), "--output-dir", str(output), "--parallel", "1", "--fast"]
    assert run(argv)[0] == 1
    assert f"Cannot process file {missing}" in caplog.text
    results = list(output.rglob("*.txt"))
    assert len(results) == 1
    assert "blacksmith" in results[0].read_text(encoding="utf-8")
    args = cli.parse_args(argv)
    options = settings.args_to_extractor(args)
    assert str(missing) in cli_utils._process_file(str(missing), args, -1, options)
    assert cli_utils._process_file(str(valid), args, -1, options) is None


def test_missing_input_directory_is_logged(tmp_path, caplog, run):
    source = tmp_path / "missing"
    run(["--input-dir", str(source), "--parallel", "1"])
    assert repr(str(source)) in caplog.text


def test_unreadable_directory_does_not_skip_readable_files(tmp_path, caplog, monkeypatch, run):
    source = tmp_path / "inputs"
    blocked = source / "blocked"
    blocked.mkdir(parents=True)
    readable = source / "readable"
    readable.mkdir()
    (readable / "page.html").write_bytes(Path(RESOURCES_DIR, "httpbin_sample.html").read_bytes())
    scandir = os.scandir

    def deny_blocked(directory):
        if directory == str(blocked):
            raise PermissionError(13, "Permission denied", directory)
        return scandir(directory)

    monkeypatch.setattr(os, "scandir", deny_blocked)
    output = tmp_path / "output"
    assert run(["--input-dir", str(source), "--output-dir", str(output), "--parallel", "1", "--fast"])[0] == 1
    assert repr(str(blocked)) in caplog.text
    results = list(output.rglob("*.txt"))
    assert len(results) == 1
    assert "blacksmith" in results[0].read_text(encoding="utf-8")


def test_pipeline_excludes_nested_destinations(tmp_path, monkeypatch):
    for name in ("original.html", "output/old.txt", "backup/page.html", "other/page.html"):
        target = tmp_path / name
        target.parent.mkdir(exist_ok=True)
        target.write_text("input")
    monkeypatch.chdir(tmp_path)
    args = cli.parse_args(
        ["--input-dir", ".", "--output-dir", "output/../output", "--backup-dir", "backup", "--parallel", "1"]
    )
    seen = []
    monkeypatch.setattr(cli_utils, "ProcessPoolExecutor", ThreadPoolExecutor)
    monkeypatch.setattr(cli_utils, "_process_file", lambda filename, **kwargs: seen.append(Path(filename).as_posix()))
    assert cli_utils.file_processing_pipeline(args) == 0
    assert set(seen) == {"original.html", "other/page.html"}


@pytest.mark.parametrize("alias_input", [False, True])
def test_directory_alias_excludes_nested_destination(tmp_path, alias_input):
    source = tmp_path / "input"
    output = source / "output"
    output.mkdir(parents=True)
    original = source / "page.html"
    original.write_text("input")
    (output / "old.txt").write_text("output")
    alias = tmp_path / "alias"
    try:
        alias.symlink_to(source if alias_input else output, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"Cannot create symlink on this system {error}")
    input_dir, output_dir = (alias, output) if alias_input else (source, alias)
    assert list(cli_utils.generate_filelist(str(input_dir), exclude_dirs=(str(output_dir),))) == [
        str(input_dir / original.name)
    ]


def test_file_processing(tmp_path):
    "One output per extractable file, every resource file type goes through the pipeline."
    source = tmp_path / "in"
    source.mkdir()
    assert cli_utils.file_processing_pipeline(cli.parse_args(["--parallel", "1", "--input-dir", str(source)])) == 0
    (source / "page.html").write_bytes(Path(RESOURCES_DIR, "httpbin_sample.html").read_bytes())
    (source / "tiny.html").write_text("<p>x</p>")
    args = cli.parse_args(["--input-dir", str(source), "-o", str(tmp_path / "out")])
    options = settings.args_to_extractor(args)
    for f in cli_utils.generate_filelist(str(source)):
        cli_utils.file_processing(f, args, -1, options)
    [result] = (tmp_path / "out").rglob("*.txt")
    assert "blacksmith" in result.read_text(encoding="utf-8")
    args = cli.parse_args(["--parallel", "1", "--input-dir", RESOURCES_DIR, "-o", str(tmp_path / "all")])
    assert cli_utils.file_processing_pipeline(args) == 0
    assert list((tmp_path / "all").rglob("*.txt"))


def test_counter_directories(tmp_path, monkeypatch):
    "Past MAX_FILES_PER_DIRECTORY files, outputs go to numbered subdirectories."
    source = tmp_path / "in"
    source.mkdir()
    for name in ("a.html", "b.html"):
        (source / name).write_bytes(Path(RESOURCES_DIR, "httpbin_sample.html").read_bytes())
    monkeypatch.setattr(cli_utils, "ProcessPoolExecutor", ThreadPoolExecutor)
    monkeypatch.setattr(cli_utils, "MAX_FILES_PER_DIRECTORY", 1)
    args = cli.parse_args(["--input-dir", str(source), "-o", str(tmp_path / "out"), "--parallel", "1"])
    assert cli_utils.file_processing_pipeline(args) == 0
    assert sorted(f.parent.name for f in (tmp_path / "out").rglob("*.txt")) == ["1", "2"]


@pytest.fixture
def fake_progress(monkeypatch):
    "Replace tqdm so the tests do not depend on it being installed."
    bar = MagicMock()
    bar.return_value.__exit__.return_value = False  # do not swallow exceptions
    monkeypatch.setattr(cli_utils, "tqdm", bar, raising=False)
    monkeypatch.setattr(cli_utils, "logging_redirect_tqdm", nullcontext, raising=False)
    monkeypatch.setattr(cli_utils, "HAS_TQDM", True)
    monkeypatch.setattr(cli, "HAS_TQDM", True)
    return bar


def test_progress_requires_tqdm(monkeypatch, capsys):
    "Without tqdm, --progress fails early during argument validation."
    monkeypatch.setattr(cli, "HAS_TQDM", False)
    monkeypatch.setattr(cli_utils, "HAS_TQDM", False)
    with pytest.raises(SystemExit):
        cli.parse_args(["--progress", "-i", "urls.txt"])
    assert "tqdm" in capsys.readouterr().err


def test_url_processing_progress(monkeypatch, tmp_path, fake_progress):
    "The bar counts every URL, whether its download succeeded or not."
    page = Path(RESOURCES_DIR, "httpbin_sample.html").read_text(encoding="utf-8")
    urls = ["https://a.example.org/ok", "https://b.example.org/missing", "https://c.example.org/ok"]

    def fake_downloads(bufferlist, download_threads, options):
        for url in bufferlist:
            yield url, page if url.endswith("ok") else None

    monkeypatch.setattr(cli_utils, "buffered_downloads", fake_downloads)
    args = cli.parse_args(["--output-dir", str(tmp_path), "--fast", "--progress"])

    assert cli_utils.url_processing_pipeline(args, add_to_compressed_dict(urls)) == 1
    fake_progress.assert_called_once_with(total=3, unit="URL")
    assert fake_progress.return_value.__enter__.return_value.update.call_count == 3


def test_archived_retry_progress(monkeypatch, tmp_path, fake_progress):
    "The archived retry gets its own bar over the failed URLs."
    page = Path(RESOURCES_DIR, "httpbin_sample.html").read_text(encoding="utf-8")
    urls = ["https://a.example.org/ok", "https://b.example.org/missing", "https://c.example.org/missing"]

    def fake_downloads(bufferlist, download_threads, options):
        for url in bufferlist:
            yield url, page if url.endswith("ok") or url.startswith("https://web.archive.org/web/20/https://b.") else None

    monkeypatch.setattr(cli_utils, "buffered_downloads", fake_downloads)
    args = cli.parse_args(["--output-dir", str(tmp_path), "--fast", "--progress", "--archived"])

    assert cli_utils.url_processing_pipeline(args, add_to_compressed_dict(urls)) == 1
    assert fake_progress.call_args_list == [((), {"total": 3, "unit": "URL"}), ((), {"total": 2, "unit": "URL"})]
    assert fake_progress.return_value.__enter__.return_value.update.call_count == 5


def test_file_processing_progress(tmp_path, caplog, monkeypatch, fake_progress):
    "The bar total comes from the processing walk: nested outputs skipped, walk errors logged once."
    source = tmp_path / "inputs"
    blocked = source / "blocked"
    blocked.mkdir(parents=True)
    page = Path(RESOURCES_DIR, "httpbin_sample.html").read_bytes()
    for name in ("one.html", "two.html", "output/old.html"):
        (source / name).parent.mkdir(exist_ok=True)
        (source / name).write_bytes(page)
    scandir = os.scandir

    def deny_blocked(directory):
        if directory == str(blocked):
            raise PermissionError(13, "Permission denied", directory)
        return scandir(directory)

    monkeypatch.setattr(os, "scandir", deny_blocked)
    args = cli.parse_args(
        ["--input-dir", str(source), "--output-dir", str(source / "output"), "--parallel", "1", "--progress"]
    )

    assert cli_utils.file_processing_pipeline(args) == 1
    fake_progress.assert_called_once_with(total=2, unit="file")
    assert fake_progress.return_value.__enter__.return_value.update.call_count == 2
    assert caplog.text.count("Cannot read input directory") == 1


@pytest.mark.parametrize("start_method", ["spawn", "forkserver"])
@pytest.mark.parametrize(
    "mode, verbosity, debug_expected",
    [
        ("cli", [], False),
        ("cli", ["-v"], False),
        ("cli", ["-vv"], True),
        ("debug", [], True),
        ("error", ["-vv"], False),
        ("unconfigured", [], False),
    ],
)
def test_file_worker_logging(tmp_path, start_method, mode, verbosity, debug_expected):
    "Fresh workers follow configured logging without changing the parent's handlers."
    if start_method not in get_all_start_methods():
        pytest.skip(f"{start_method} is not available on this platform")
    source = tmp_path / "input"
    source.mkdir()
    (source / "page.html").write_text("<html><body><p>" + "Some text here. " * 50 + "</p></body></html>", encoding="utf-8")
    output = tmp_path / "output"
    script = """import logging
import multiprocessing
import sys
from trafilatura import cli, cli_utils

if __name__ == "__main__":
    multiprocessing.set_start_method(sys.argv[1])
    mode = sys.argv[2]
    root = logging.getLogger()
    if mode in ("debug", "error"):
        level = logging.DEBUG if mode == "debug" else logging.ERROR
        logging.basicConfig(stream=sys.stderr, level=level, format="parent:%(levelname)s:%(message)s")
    handlers = list(root.handlers)
    level = root.level
    args = cli.parse_args(sys.argv[3:])
    if mode == "unconfigured":
        assert cli_utils.file_processing_pipeline(args) == 0
    else:
        cli.process_args(args)
    if mode != "cli":
        assert root.handlers == handlers and root.level == level
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            start_method,
            mode,
            "--input-dir",
            str(source),
            "--output-dir",
            str(output),
            "--parallel",
            "1",
            *verbosity,
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    assert ("DEBUG:trafilatura.main_extractor:Recovering wild text elements" in result.stderr) is debug_expected
    assert result.stdout == ""
    files = list(output.glob("*.txt"))
    assert len(files) == 1
    assert "Some text here." in files[0].read_text(encoding="utf-8")


def test_crawling(capsys, run):
    cli_utils.cli_crawler(cli.parse_args(["--crawl", " "]))

    assert run(["--crawl", "https://httpbun.com/html"])[1] == "https://httpbun.com/html\n"

    # links permitted
    args = cli.parse_args(["--crawl", "https://httpbun.com/links/1/1", "--list", "--parallel", "1"])
    cli_utils.cli_crawler(args)
    # possibly a bug on Github actions, should be 2 URLs
    assert capsys.readouterr().out in (
        "https://httpbun.com/links/1/1\nhttps://httpbun.com/links/1/0\n",
        "https://httpbun.com/links/1/1\n",
    )
    # 0 links permitted
    args.URL = "https://httpbun.com/links/4/4"
    cli_utils.cli_crawler(args, n=0)
    ## should be 6 (5 URLs as output), possibly a bug on Actions CI/CD
    assert len(capsys.readouterr().out.split("\n")) in (2, 6)

    # responses from an unregistered base (e.g. cross-host redirect) are skipped
    start = fetch_response("https://httpbun.com/links/2/2")
    extra = [
        ("https://stray.example/", Response(b"<html><body><a href='/x'>x</a></body></html>", 200, "https://stray.example/")),
        (start.url, start),
    ]
    real_downloads = cli_utils.buffered_response_downloads

    def with_stray(bufferlist, threads, options=None):
        while extra:
            yield extra.pop()
        yield from real_downloads(bufferlist, threads, options=options)

    args = cli.parse_args(["--crawl", "https://httpbun.com/links/2/2", "--list"])
    with patch.object(cli_utils, "buffered_response_downloads", with_stray):
        with patch.object(cli_utils.LOGGER, "warning") as mock_warning:
            cli_utils.cli_crawler(args)
    mock_warning.assert_called_once_with("no crawl parameters for %s", "https://stray.example/")
    assert "https://httpbun.com/links/2/0" in spider.URL_STORE.find_known_urls("https://httpbun.com")
    assert not spider.URL_STORE.find_known_urls("https://stray.example")

    # Exploration (Sitemap + Crawl)
    assert run(["--explore", "https://httpbun.com/html", "--list"])[1].strip() == "https://httpbun.com/html"


def test_blacklist_discovered_urls(tmp_path, run):
    "The blacklist also applies to the URLs found by feeds, sitemaps and the crawler."
    blacklist = tmp_path / "blacklist.txt"
    blacklist.write_text(
        "https://example.org/drop\nhttps://httpbun.com/links/2/0/\nhttps://httpbun.com/html\n", encoding="utf-8"
    )

    for option, function in (("--feed", "find_feed_urls"), ("--sitemap", "sitemap_search")):
        found = ["https://example.org/drop", "https://example.org/keep"]
        with patch.object(cli_utils, function, return_value=found):
            code, out, _ = run([option, "https://example.org/", "--list", "-b", str(blacklist)])
        assert code == 0
        assert out == "https://example.org/keep\n"

    # links followed by the crawler
    out = run(["--explore", "https://httpbun.com/links/2/2", "--list", "-b", str(blacklist)])[1]
    assert "https://httpbun.com/links/2/1" in out
    assert "https://httpbun.com/links/2/0" not in out

    # start URL of a crawl
    code, out, _ = run(["--crawl", "https://httpbun.com/html", "--list", "-b", str(blacklist)])
    assert code == 1
    assert out.strip() == ""


def test_probing(run):
    url = "https://example.org/"
    conf = path.join(RESOURCES_DIR, "zerolength.cfg")
    argv = ["--probe", url, "--config-file", conf, "--target-language"]
    if LANGID_FLAG:
        assert run([*argv, "de"])[1].strip() == ""
    assert run([*argv, "en"])[1].strip() == url


def test_probing_wrong_language(capsys):
    "A page in another language than --target-language is not printed."
    html = f"<html><body><p>{'Some English text. ' * 20}</p></body></html>"
    args = cli.parse_args(["--probe", "https://example.org/", "--target-language", "de"])
    with (
        patch.object(cli_utils, "buffered_downloads", return_value=[("https://example.org/", html)]),
        patch.object(cli_utils, "LANGID_FLAG", True),
        patch.object(cli_utils, "language_classifier", return_value="en"),
    ):
        assert cli_utils.probe_homepage(args) == 0
    assert capsys.readouterr().out == ""


def test_probing_undetectable_language(capsys):
    "A --target-language the detector cannot output does not filter, as documented."
    html = f"<html><body><p>{'Some English text. ' * 20}</p></body></html>"
    args = cli.parse_args(["--probe", "https://example.org/", "--target-language", "zz"])
    with (
        patch.object(cli_utils, "buffered_downloads", return_value=[("https://example.org/", html)]),
        patch.object(cli_utils, "LANGID_FLAG", True),
        patch.object(cli_utils, "detectable_languages", return_value={"de", "en"}),
        patch.object(cli_utils, "language_classifier", return_value="en"),
    ):
        assert cli_utils.probe_homepage(args) == 0
    assert capsys.readouterr().out == "https://example.org/\n"


@pytest.mark.parametrize("relative_input", [False, True])
def test_keep_dirs_local_batch(tmp_path, monkeypatch, relative_input):
    """Kept paths stay relative to the input directory, beneath the output directory."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    monkeypatch.chdir(tmp_path)
    input_arg = Path("input") if relative_input else input_dir
    args = cli.parse_args(["--input-dir", str(input_arg), "--output-dir", str(output_dir), "--keep-dirs"])
    for relative_path in (Path("article.html"), Path("nested", "article.txt")):
        output_path, destination_dir = cli_utils.determine_output_path(args, str(input_arg / relative_path), "")
        expected = output_dir / relative_path.with_suffix(".txt")
        assert output_path == str(expected)
        assert destination_dir == str(expected.parent)


@pytest.mark.parametrize("output_format", ["html", "xml"])
def test_keep_dirs_never_overwrites_input_file(tmp_path, caplog, monkeypatch, output_format):
    """An input file whose output path is the file itself is skipped with an error, the rest is written."""
    source = tmp_path / "in"
    (source / "nested").mkdir(parents=True)
    html = Path(RESOURCES_DIR, "httpbin_sample.html").read_bytes()
    clashing = source / f"a.{output_format}"
    clashing.write_bytes(html)
    (source / "nested" / "b.htm").write_bytes(html)
    args = cli.parse_args(
        ["--input-dir", str(source), "-o", str(source), "--keep-dirs", f"--{output_format}", "--parallel", "1", "--fast"]
    )
    # run the workers in-process so that their log records reach caplog
    monkeypatch.setattr(cli_utils, "ProcessPoolExecutor", ThreadPoolExecutor)
    assert cli_utils.file_processing_pipeline(args) == 0
    assert clashing.read_bytes() == html
    assert f"Skipping {clashing}: the output path would overwrite the input file" in caplog.text
    written = source / "nested" / f"b.{output_format}"
    assert "blacksmith" in written.read_text(encoding="utf-8")


@pytest.mark.parametrize("option", ["-o", "--backup-dir"])
def test_unwritable_output_dir_stops_early(tmp_path, option, run):
    (tmp_path / "blocker").write_text("")
    with patch.object(cli, "file_processing_pipeline") as pipeline:
        run(["--input-dir", str(tmp_path), option, str(tmp_path / "blocker" / "out")])
    pipeline.assert_not_called()


@pytest.mark.parametrize("option, func", [("--crawl", "cli_crawler"), ("--probe", "probe_homepage")])
def test_printing_modes_create_no_output_dir(tmp_path, option, func, run):
    with patch.object(cli, func, return_value=0):
        assert run([option, "https://example.org/", "-o", str(tmp_path / "out")])[0] == 0
    assert not (tmp_path / "out").exists()


def test_crawler_skips_domains_without_start_page():
    "Discarded domains and domains with only visited URLs are not crawled."
    url_store = UrlStore()
    url_store.add_urls(["https://discarded.org/x"])
    url_store.discard(["https://discarded.org"])
    url_store.add_urls(["https://visited.org/x"], visited=True)
    with patch.object(spider, "init_crawl") as init_crawl:
        assert cli_utils.cli_crawler(cli.parse_args([]), url_store=url_store) == 1
    init_crawl.assert_not_called()


def test_cli_stdin_rejected(run):
    with patch("sys.stdin") as mock_stdin:
        mock_stdin.buffer.read.return_value = b"<p>x</p>"
        err = run([])[2]
    assert "ERROR: file size" in err


@pytest.mark.parametrize(
    "argv, message",
    [
        (["-i", "missing.txt"], "-i/--input-file: No such file or directory"),
        (["-u", "https://example.org", "-b", "missing.txt"], "-b/--blacklist: No such file or directory"),
        (["-u", "https://example.org", "--config-file", "missing.cfg"], "--config-file: No such file or directory"),
        (["-i", "."], "-i/--input-file: not a file"),
        (["-u", "https://example.org", "-b", "."], "-b/--blacklist: not a file"),
        (["-u", "https://example.org", "--config-file", "."], "--config-file: not a file"),
        (["--input-dir", ".", "--parallel", "0"], "--parallel must be a positive integer"),
        (["-u", "https://example.org", "-o", "out", "--keep-dirs"], "--keep-dirs requires --input-dir"),
        (["--keep-dirs"], "--keep-dirs requires --input-dir"),
        (["--name-from-url", "-u", "https://example.org/"], "--name-from-url requires"),
        *(
            (["--name-from-url", "-o", "output", *extra], "--name-from-url requires")
            for extra in (
                [],
                ["--keep-dirs"],
                ["--input-dir", "input"],
                ["--crawl", "https://example.org"],
                ["--probe", "https://example.org"],
            )
        ),
        *(
            ([option, *extra], message)
            for option in ("--feed", "--sitemap", "--crawl", "--explore", "--probe")
            for extra, message in (
                ([], "requires a URL"),
                ([""], "requires a URL"),
                (["https://example.org", "--input-dir", "input"], "cannot be combined with --input-dir"),
                (["https://example.org", "-u", "https://example.net"], "give the URL once"),
                (["https://example.org", "-i", path.join(RESOURCES_DIR, "list-process.txt")], "give the URL once"),
            )
        ),
    ],
)
def test_invalid_args_exit_code(tmp_path, monkeypatch, run, argv, message):
    monkeypatch.chdir(tmp_path)
    code, _, err = run(argv)
    assert code == 2
    assert message in err


@pytest.mark.parametrize("option", ["--feed", "--sitemap", "--crawl", "--explore", "--probe"])
def test_navigation_url_forms(option):
    for argv in (
        [option, "https://example.org"],
        [option, "-u", "https://example.org"],
        [option, "", "-u", "https://example.org"],
    ):
        args = cli.parse_args(argv)
        assert args.URL == "https://example.org"
        assert getattr(args, option[2:]) is True
    args = cli.parse_args([option, "", "-i", path.join(RESOURCES_DIR, "list-process.txt")])
    assert args.URL is None
    assert getattr(args, option[2:]) is True


def test_input_file_first_token(tmp_path, caplog):
    urls = tmp_path / "urls.txt"
    urls.write_text(
        "https://example.org/a some note\n\n  https://example.org/b\tnote\nhttps://example.org/c\u00a0d\n", encoding="utf-8"
    )
    args = cli.parse_args(["-i", str(urls)])
    assert cli_utils.load_input_urls(args) == [
        "https://example.org/a",
        "https://example.org/b",
        "https://example.org/c\u00a0d",
    ]
    urls.write_text("\n  \n", encoding="utf-8")
    with caplog.at_level(logging.WARNING):
        assert cli_utils.load_input_urls(args) == []
    assert "No input provided" in caplog.text


def test_keep_dirs_strips_extensions(tmp_path):
    "Only a final lowercase extension is stripped, so distinct inputs keep distinct outputs."
    args = cli.parse_args(["--input-dir", str(tmp_path), "-o", str(tmp_path / "out"), "--keep-dirs"])
    for name, expected in (
        ("c.html", "c.txt"),
        ("c.html.gz", "c.html.txt"),
        ("Mr.Smith", "Mr.Smith.txt"),
        ("v1.2.htm", "v1.2.txt"),
        ("a.gz", "a.txt"),
    ):
        output_path, _ = cli_utils.determine_output_path(args, str(tmp_path / name), "")
        assert Path(output_path).name == expected


def test_list_input_dir_notice(capsys):
    cli.parse_args(["--input-dir", ".", "--list", "--json"])
    err = capsys.readouterr().err
    assert "--list has no effect on --input-dir" in err
    assert "options are ignored" not in err


@pytest.mark.parametrize("list_mode", [False, True], ids=["extract", "list"])
def test_discovery_processes_found_urls_only(list_mode, capsys):
    found = ["https://example.org/news/a", "https://example.org/news/b"]
    processed = []
    with (
        patch.object(cli_utils, "sitemap_search", lambda url, **kwargs: found),
        patch.object(cli_utils, "url_processing_pipeline", lambda args, store: processed.extend(store.dump_urls()) or 0),
    ):
        argv = ["--sitemap", "https://example.org/sitemap.xml"] + (["--list"] if list_mode else [])
        assert cli_utils.cli_discovery(cli.parse_args(argv)) == 0
    assert sorted(processed + capsys.readouterr().out.split()) == found


@pytest.mark.parametrize("option", ["--feed", "--sitemap"])
@pytest.mark.parametrize("found", [{}, {"https://a.org/": ["https://a.org/x"]}])
def test_discovery_without_links_exit_code(tmp_path, option, found):
    "Seeds without links are errors but not download failures: exit 1, never 126."
    (tmp_path / "seeds").write_text("https://a.org/\nhttps://b.org/\n", encoding="utf-8")
    search = "find_feed_urls" if option == "--feed" else "sitemap_search"
    with (
        patch.object(cli_utils, search, lambda url, **kwargs: found.get(url, [])),
        patch.object(cli_utils, "url_processing_pipeline", lambda args, store: 0),
    ):
        assert cli_utils.cli_discovery(cli.parse_args([option, "-i", str(tmp_path / "seeds")])) == 1


def test_url_filter_discarding_all_inputs(caplog):
    with patch.object(cli_utils, "sitemap_search") as search:
        assert cli_utils.cli_discovery(cli.parse_args(["--sitemap", "https://example.org/", "--url-filter", "/news/"])) == 1
    search.assert_not_called()
    assert "No input URL left" in caplog.text


def test_config_file_with_bom(tmp_path):
    conf = tmp_path / "bom.cfg"
    conf.write_text("[DEFAULT]\nMIN_OUTPUT_SIZE = 12345\n", encoding="utf-8-sig")
    assert settings.use_config(str(conf)).getint("DEFAULT", "MIN_OUTPUT_SIZE") == 12345


@pytest.mark.parametrize("option", ["--sitemap", "--explore"])
def test_discovery_duplicate_links(tmp_path, option):
    "A seed whose links were already found for another seed has links."
    seeds = tmp_path / "seeds.txt"
    seeds.write_text("https://example.org/a\nhttps://example.org/b\n")
    links = ["https://example.org/x", "https://example.org/y"]
    with (
        patch.object(cli_utils, "sitemap_search", return_value=links),
        patch.object(cli_utils, "url_processing_pipeline", return_value=0) as pipeline,
        patch.object(cli_utils, "cli_crawler") as crawler,
    ):
        assert cli_utils.cli_discovery(cli.parse_args(["-i", str(seeds), option, "--parallel", "1"])) == 0
    crawler.assert_not_called()
    assert sorted(pipeline.call_args.args[1].dump_urls()) == links


@pytest.mark.parametrize("list_mode", [False, True], ids=["extract", "list"])
def test_explore_crawls_seeds_without_links(tmp_path, list_mode):
    "Only seeds without links left after the blacklist are crawled, also after --list flushed the store."
    seeds = tmp_path / "seeds.txt"
    seeds.write_text("https://a.org/\nhttps://b.org/\nhttps://nolinks.org/\nhttps://blocked.org/\n")
    blacklist = tmp_path / "blacklist.txt"
    blacklist.write_text("https://blocked.org/page\n")
    crawled = []
    with (
        patch.object(cli_utils, "sitemap_search", lambda url, **kwargs: [] if "nolinks" in url else [url + "page"]),
        patch.object(cli_utils, "url_processing_pipeline", lambda args, store: 0),
        patch.object(cli_utils, "cli_crawler", lambda args, url_store, options: crawled.extend(url_store.dump_urls()) or 0),
    ):
        args = cli.parse_args(
            ["-i", str(seeds), "-b", str(blacklist), "--explore", "--parallel", "1"] + (["--list"] if list_mode else [])
        )
        args.blacklist = cli_utils.load_blacklist(args.blacklist)
        assert cli_utils.cli_discovery(args) == 0
    assert sorted(crawled) == ["https://blocked.org/", "https://nolinks.org/"]
