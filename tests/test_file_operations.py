import pytest
from note_taking.models import RenameResult, FileProcessResult
from note_taking.file_operations import process_file, update_file_references, update_files_and_backlinks

# Utility function to read files
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

# Fixtures for test data
@pytest.fixture
def create_link_test_file(tmp_path):
    content = """
    # Sample Markdown

    This is a sample markdown file. Here is a link [[project.work-a.meeting.conference-call]] and
    here is another with an alias [[project.work-a.meeting.conference-call|important meeting]]
    """
    file_path = tmp_path / "link_test.md"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return file_path

@pytest.fixture
def create_overall_test_files(tmp_path):
    # First file
    content_1 = """
    # Calendar

    - 2022-01-01 Did this meeting about [[project.company.main_idea]]
    """
    calendar_path = tmp_path / "calendar.md"
    with open(calendar_path, 'w', encoding='utf-8') as file:
        file.write(content_1)

    # Second file
    content_2 = """
    # Sample Markdown

    Meeting notes
    """
    sub_folder = tmp_path / "sub-folder"
    sub_folder.mkdir()
    project_file_path = sub_folder / "project.company.main_idea.md"
    with open(project_file_path, 'w', encoding='utf-8') as file:
        file.write(content_2)

    return tmp_path

# The tests
def test_process_file_match():
    root = "./notes/"
    filename = "project.work-a.meetings.meetings-on-this-day.md"
    keyword = "project.work-a"
    replacement = "project.work-b"

    expected_result = FileProcessResult(True, "./notes/project.work-a.meetings.meetings-on-this-day.md", "project.work-a.meetings.meetings-on-this-day", "./notes/project.work-b.meetings.meetings-on-this-day.md", "project.work-b.meetings.meetings-on-this-day")
    assert process_file(root, filename, keyword, replacement) == expected_result

def test_process_file_nonmatch():
    root = "./notes/"
    filename = "project.work-z.meetings.meetings-on-this-day.md"
    keyword = "project.work-a"
    replacement = "project.work-b"

    expected_result = FileProcessResult(False, "./notes/project.work-z.meetings.meetings-on-this-day.md", "project.work-z.meetings.meetings-on-this-day", "./notes/project.work-z.meetings.meetings-on-this-day.md", "project.work-z.meetings.meetings-on-this-day")
    assert process_file(root, filename, keyword, replacement) == expected_result

def test_replace_links(create_link_test_file):
    update_file_references(create_link_test_file, "project.work-a", "project.work-b")

    input_markdown = read_file(create_link_test_file)
    expected_output_markdown = """
    # Sample Markdown

    This is a sample markdown file. Here is a link [[project.work-b.meeting.conference-call]] and
    here is another with an alias [[project.work-b.meeting.conference-call|important meeting]]
    """
    
    assert input_markdown.strip() == expected_output_markdown.strip(), "The markdown output did not match the expected output."

def test_overall(create_overall_test_files):
    # Dynamically generate expected file paths based on the temporary directory
    project_file_path = create_overall_test_files / "sub-folder" / "project.company.main_idea.md"
    archive_file_path = create_overall_test_files / "sub-folder" / "archive.project.company.main_idea.md"

    expected_result = RenameResult(
        [FileProcessResult(
            change_flag=True,
            old_full_file_path=str(project_file_path),
            old_base='project.company.main_idea',
            new_full_file_path=str(archive_file_path),
            new_base='archive.project.company.main_idea'
        )],1,1)

    assert update_files_and_backlinks(
        "project.company.main_idea",
        "archive.project.company.main_idea",
        action=True,
        dir_path=create_overall_test_files
    ) == expected_result