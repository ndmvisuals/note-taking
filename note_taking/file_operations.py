import os
import fileinput
import re
from pathlib import Path
from note_taking.utils import filter_hidden_directories
from note_taking.config import BASE_DIR
from note_taking.models import RenameResult, FileProcessResult


def rename_file(original_file_path, new_file_path):
    os.rename(original_file_path, new_file_path)



def process_file(root: str, filename: str, keyword: str, replacement:str) -> FileProcessResult:
    '''
    This function determines if a file needs to be renamed based on the filename and the pattern we are looking to rename.

    Parameters:
    - root (str): the root of the file name
    - filename (str): the filename
    - keyword (str): the part of the file name heiarchy that needs to be replaced
    - replacement (str): the file name heiarchy that will replace the old pattern

    Returns:
    - FileProcessResult Method
    
    
    '''
    change_flag = False
    new_filename = filename
    new_path = os.path.join(root, new_filename)
    old_path = os.path.join(root, filename)
    old_base, _ = os.path.splitext(filename)
    new_base, _ = os.path.splitext(filename)
    
    if keyword in filename:
        new_filename = filename.replace(keyword, replacement)
        new_path = os.path.join(root, new_filename)
        new_base, _ = os.path.splitext(new_filename)
        change_flag = True

    return FileProcessResult(change_flag, old_path, old_base, new_path, new_base)

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

    return(number_of_links_changed)

def update_files_and_backlinks(keyword: str, replacement: str, action = False, dir_path = BASE_DIR) -> RenameResult:
    files_to_rename = []
    # Rename files
    # ============
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = filter_hidden_directories(dirs)
        for filename in files:
            if filename.endswith((".md", ".txt", ".qmd", ".canvas")):
                result = process_file(root, filename, keyword, replacement)
                if result.change_flag:
                    if action == True:
                        rename_file(result.old_full_file_path, result.new_full_file_path)
                        files_to_rename.append(result)
                    else:
                        files_to_rename.append(result)


    # Rename Links
    # ------------
    total_links_updated = 0
    for root, dirs, files in os.walk(dir_path):
        

        dirs[:] = filter_hidden_directories(dirs)
        
        for filename in files:
            if filename.endswith((".md", ".txt", ".qmd", ".canvas")):
                full_path = os.path.join(root, filename)
                for rename in files_to_rename:
                    if action == True:
                        n_links_updated = update_file_references(full_path, rename.old_base, rename.new_base)
                        total_links_updated = total_links_updated + n_links_updated
                    else:
                        pass
            
                


                
    return RenameResult(files_to_rename, len(files_to_rename) ,total_links_updated, )





    
