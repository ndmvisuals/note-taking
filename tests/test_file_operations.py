from note_taking.models import RenameResult, FileProcessResult
from note_taking.file_operations import process_file, update_file_references, update_files_and_backlinks

# Utility functions for tests
# ===========================
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
    
# Create data for link test
content = """
# Sample Markdown

This is a sample markdown file. Here is a link [[project.work-a.meeting.conference-call]] and
here is another with an alias [[project.work-a.meeting.conference-call|important meeting]]
"""

with open("./tests/replace_links_test/test_data/link_test.md", 'w', encoding='utf-8') as file:
        file.write(content)

# Create data for final all in one test

# First
content_1 = """
# Calendar

- 2022-01-01 Did this meeting about [[project.company.main_idea]]
"""

with open("./tests/overall_test_data/calendar.md", 'w', encoding='utf-8') as file:
        file.write(content_1)


# Second
content_2 = """
# Sample Markdown

Meeting notes
"""

with open("./tests/overall_test_data/sub-folder/project.company.main_idea.md", 'w', encoding='utf-8') as file:
        file.write(content_2)





    
# The tests
# ===========

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

def test_replace_links():
    # Make the reference change
    update_file_references("./tests/replace_links_test/test_data/link_test.md", "project.work-a", "project.work-b")

    # Read in files to compare
    # ======================
    input_markdown = read_file("./tests/replace_links_test/test_data/link_test.md")
    expected_output_markdown = read_file("tests/replace_links_test/result_data/link_result.md")


    # Assert that the processed output matches the expected output
    assert input_markdown == expected_output_markdown, "The markdown output did not match the expected output."
    

def test_overall():
      expected_result = RenameResult([FileProcessResult(True,"./tests/overall_test_data/sub-folder/project.company.main_idea.md", "project.company.main_idea", "./tests/overall_test_data/sub-folder/archive.project.company.main_idea.md", "archive.project.company.main_idea"  )], 1, 1)
      assert update_files_and_backlinks("project.company.main_idea", "archive.project.company.main_idea", action = True, dir_path = "./tests/overall_test_data/")  == expected_result


