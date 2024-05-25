from note_taking.utils import filter_hidden_directories

def test_filter_hidden_directories():
    dirs = ['.hidden', 'visible', '.another_hidden']
    expected_result = ['visible']
    assert filter_hidden_directories(dirs) == expected_result

