import os
import fileinput
import re
from pathlib import Path
from note_taking.config import BASE_DIR
from note_taking.models import RenameResult, FileProcessResult

def keyword_rename(keyword: str, replacement: str, action: bool = False) -> RenameResult:
    files_to_rename = []
    number_of_links_changed = 0

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = filter_hidden_directories(dirs)
        
        for filename in files:
            result = process_file(root, filename, keyword, replacement, action)
            if result.change_flag:
                files_to_rename.append({"original": result.full_path, "change": os.path.join(root, result.new_filename)})
                if action:
                    number_of_links_changed += update_file_references(result.full_path, keyword, replacement)
                
    return RenameResult(files_to_rename=files_to_rename, number_of_links_changed=number_of_links_changed)

def filter_hidden_directories(dirs):
    return [d for d in dirs if not d.startswith('.')]

def process_file(root, filename, keyword, replacement, action) -> FileProcessResult:
    change_flag = False
    new_filename = filename
    full_path = os.path.join(root, filename)
    
    if filename.endswith((".md", ".txt", ".qmd")) and keyword in filename:
        new_filename = filename.replace(keyword, replacement)
        change_flag = True
        if action:
            os.rename(full_path, os.path.join(root, new_filename))
    
    return FileProcessResult(change_flag, new_filename, full_path)

def update_file_references(full_path, keyword, replacement):
    number_of_links_changed = 0
    with fileinput.FileInput(full_path, inplace=True) as file:
        for line in file:
            pattern = re.compile(r'\[\[(.*?)\]\]')
            matches = pattern.findall(line)
            
            for match in matches:
                new_match = match.replace(keyword, replacement)
                if f"[[{match}]]" != f"[[{new_match}]]":
                    line = line.replace(f"[[{match}]]", f"[[{new_match}]]")
                    number_of_links_changed += 1
            
            print(line, end="")
    return number_of_links_changed
