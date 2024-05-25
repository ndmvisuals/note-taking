from dataclasses import dataclass
from typing import List

@dataclass
class RenameResult:
    files_to_rename: List[dict]
    number_of_links_changed: int

@dataclass
class FileProcessResult:
    change_flag: bool
    new_filename: str
    full_path: str
