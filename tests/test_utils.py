from rcpack import utils


def test_get_language_from_extension_path_and_ext():
    # file path
    assert utils.get_language_from_extension('src/main.py') == 'python'
    # extension with leading dot
    assert utils.get_language_from_extension('.js') == 'javascript'
    # extension without dot
    assert utils.get_language_from_extension('ts') == 'typescript'
    # unknown extension returns empty string
    assert utils.get_language_from_extension('.unknownext') == ''


def test_calculate_total_lines_and_characters():
    files = {
        'a.txt': 'line1\nline2\n',
        'b.txt': 'singleline'
    }

    # total lines: a.txt has 2 lines, b.txt has 1 line -> 3
    assert utils.calculate_total_lines(files) == 3
    # total characters: length of both strings
    assert utils.calculate_total_characters(files) == len('line1\nline2\n') + len('singleline')
