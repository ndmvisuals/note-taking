from dataclasses import dataclass
from typing import List


@dataclass
class FileProcessResult:
    change_flag: bool
    old_full_file_path: str
    old_base: str
    new_full_file_path: str
    new_base: str


@dataclass
class RenameResult:
    files_to_rename: List[FileProcessResult]
    number_files_updated: int
    number_of_links_changed: int

