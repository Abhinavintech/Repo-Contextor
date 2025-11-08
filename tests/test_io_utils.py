from pathlib import Path
from rcpack import io_utils


def test_write_output_and_is_binary_file(tmp_path: Path):
    out_dir = tmp_path / "nested" / "dir"
    out_file = out_dir / "out.txt"

    # write_output should create parent directories and write content
    io_utils.write_output(str(out_file), "hello world")
    assert out_file.exists()
    assert out_file.read_text(encoding="utf-8") == "hello world"

    # create a small binary file containing a NUL byte
    bin_file = tmp_path / "bin.dat"
    bin_file.write_bytes(b"\x00\x01\x02")
    assert io_utils.is_binary_file(bin_file) is True


def test_read_text_safely_truncation_and_encoding(tmp_path: Path):
    # create a large UTF-8 file to trigger truncation
    large_file = tmp_path / "large.txt"
    content = "a" * (16_384 + 100)
    large_file.write_text(content, encoding="utf-8")

    text, enc, truncated = io_utils.read_text_safely(large_file, max_bytes=16_384)
    assert truncated is True
    assert enc in ("utf-8", "utf-8")
    assert len(text.encode(enc)) <= 16_384

    # create a file that's valid utf-16
    utf16_file = tmp_path / "u16.txt"
    utf16_file.write_bytes("helloworld".encode("utf-16"))
    text2, enc2, truncated2 = io_utils.read_text_safely(utf16_file)
    assert truncated2 is False
    assert enc2 in ("utf-16", "utf-16-le", "utf-16-be")
    assert "helloworld" in text2
